# Copyright (C) 2019  NCC Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import sys,os
import frida
import winstrument.utils as utils
from colorama import Fore, Back, Style
import threading
from frida_tools.application import Reactor
import importlib, pkgutil
import sqlite3
import json
import toml
from winstrument.db_connection import DBConnection
from winstrument.settings_controller import SettingsController
from winstrument.data.module_message import ModuleMessage
from datetime import datetime

class Winstrument():
    #adapted from https://github.com/frida/frida-python/blob/master/examples/child_gating.py
    CORE_MODNAME = "core"

    def __init__(self):
        appdata_path = os.environ["appdata"]
        data_path = os.path.join(appdata_path,"winstrument")

        if not os.path.exists(data_path):
            os.mkdir(data_path)

        settings_path = os.path.join(data_path, "settings.toml")

        #unique temporary storage for each instance of the program
        self._db = DBConnection(os.path.join(data_path,f"db_{datetime.now().timestamp()}.sqlite3"))
        self.settings_controller = SettingsController(settings_path)
        default_settings = {'target': 'C:\\Windows\\System32\\Calc.exe' , "verbosity": 0}
        #settings won't exist on first run
        if self.settings_controller.get_module_settings(self.CORE_MODNAME) == {}:
            self.settings_controller.set_module_settings(self.CORE_MODNAME, default_settings)

        self.metadata = self.get_metadata()
        self._stop_requested = threading.Event()
        self._reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())
        self._device = frida.get_local_device()
        self._sessions = set()

        self._device.on("child-added", lambda child: self._reactor.schedule(lambda: self._on_child_added(child)))
        self._device.on("child-removed", lambda child: self._reactor.schedule(lambda: self._on_child_removed(child)))
        self._base_module = importlib.import_module("winstrument.base_module",None)
        self._modules_to_load=[]
        self._available_modules = self._enumerate_modules()
        self._loaded_modules = []
        self._instrumentations = []

    def get_metadata(self, filename="metadata.toml"):
        """
        Parse the metadata.toml file for module metadata like descriptions, if present.
        Returns dict of metadata, or None if the file is not present or invalid.
        """

        metadata_filepath = os.path.join(os.path.dirname(__file__),"modules",filename)
        try:
            metadata = toml.load(metadata_filepath)
            return dict((k.lower(), v) for k,v in metadata.items()) #modulenames are lowercase

        except toml.TomlDecodeError:
            metadata = None
        return metadata

    def get_available_modules(self):
        """
        Gets a list of all available modules (from modules/metadata.toml)
        returns a list with module names
        """
        return self._available_modules.copy()

    def get_loaded_modules(self):
        """
        Gets a list of all modules that have already been loaded
        returns a list of module names
        """
        return [mod for mod in self._loaded_modules]

    def export_all(self, outfile, formatter=utils.format_table):
        """
        Write the output for all modules to the given output stream in the desired format
        outfile - file stream object. This could be a normal file or sys.stdout
        formatter - callable which takes a list of ModuleMessage objects and returns a string to output. See utils.py
        No return, but writes the output stream
        """

        for module in self.get_available_modules():
            self.print_saved_output(module,formatter,outfile)

    def print_saved_output(self, modulename, formatter=utils.format_table, output=sys.stdout):
        """
        Write the output for the given module to the given output stream in the desired format.
        modulename - str
        formatter - callable which takes a list of ModuleMessage objects and returns a string to output. See utils.py
        output - file stream object. This could be a normal file or sys.stdout
        No return, but writes the output stream
        """
        messages = self._db.read_messages(modulename)
        if formatter is None:
            formatter = utils.format_table
        verbosity = self.settings_controller.get_setting_int(self.CORE_MODNAME,"verbosity") or 0
        output.write(formatter(messages,verbosity)+"\n")

    def unload_module(self, module):
        """
        Unloads the given module. It will not be injected with the target is run
        module - str
        """
        try:
            self._modules_to_load.remove(module)
            self._loaded_modules.remove(module)
        except ValueError:
            print (f"Can't unload because {module} wasn't loaded")
        if module not in self._available_modules:
            self._available_modules.append(module)
        self._initialize_modules()

    def load_module(self, module):
        """
        Loads the given module, if it hasn't already been loaded.
        modulename - str
        """
        if module not in self._modules_to_load:
            self._modules_to_load.append(module)
        else:
            print(f"Error: {module} is already loaded")
            return
        self._initialize_modules()

    def _enumerate_modules(self,moudlepath="modules"):
        """
        Returns a list of available modules. Uses metadata file if available, otherwise falls back to all modules in the modulepath
        """
        if self.metadata:
            available_modules = [key.lower() for key in self.metadata.keys()]
        else: #metadata file missing or broken, fall back to module discovery based on path
            available_modules = [name for _, name, _, in pkgutil.iter_modules([os.path.join(os.path.dirname(__file__), moudlepath)])]
        return available_modules

    def _initialize_modules(self, modulepath = "winstrument.modules"):
        """
        Import python modules that are set to be loaded. If the module is not found, print a warning to STDOUT and remove the module from the _modules_to_load list.
        modulepath: string - Python import path for modules. This is a Python path, not a Windows path.
        """
        for modulename in self._modules_to_load:
            try:
                module = importlib.import_module(f"{modulepath}.{modulename}")
                if module not in self._loaded_modules:
                    self._loaded_modules.append(modulename)

            except ImportError:
                print(f"Error: module '{modulename}' not found, skiping!")
                self._modules_to_load.remove(modulename)
                continue

    def run(self,target=None,arglist=None):
        """
        Schedule frida to spawn the target process, then instrument it.
        target: str - path to target to spawn
        arglist: list - arguments to pass to target when spawned
        """
        if target:
            process = target
            args = arglist
        else:
            process = self.settings_controller.get_setting(self.CORE_MODNAME,"target")
            args = self.settings_controller.get_setting(self.CORE_MODNAME,"args")
        self._reactor.schedule(lambda: self._start(process,args))
        self._reactor.run()

    def _start(self,target,args=None):
        """
        Spawn the target process and then instrument it with any available scripts.
        If not found, write a warning to STDERR.
        target: str - Path to the process to spawn
        args: list or None - list of command line arguments to use with the target
        """
        if target is None:
            sys.stderr.write(f"{Fore.RED} No target set. Use 'set target <target> to specify a program to instrument.\n{Style.RESET_ALL}")
            self.stop()
            return
        cmd = [target]
        if args:

            cmd.append(args)
        try:
            pid = self._device.spawn(cmd)
        except frida.ExecutableNotFoundError:
            sys.stderr.write(f"{Fore.RED}Target {target} not found! Make sure the path is correct.\n{Style.RESET_ALL}")
            self.stop()
            return
        print("Spawned " + str(pid))
        self._instrument(pid, target)

    def _stop_if_idle(self):
        """
        Helper function used with Frida reactor. Stops the reactor if there are no queued child sessions.
        """
        if len(self._sessions) == 0:
            self.stop()

    def stop(self):
        """
        Signal that the Frida reactor has been requested to stop, then stop it.
        """
        self._stop_requested.set()
        self._reactor.stop()

    def quit(self):
        """
        Save settings to settings file.
        """
        self.settings_controller.save_settings()
        self._db.close()

    def _instrument(self, pid, path):
        """
        Iterates over currently loaded modules and performs instrumentation on the target process for each.
        pid: int - PID of the spawned process
        path: str - filesystem path to the spawned process executable.
        """
        try:
            session = self._device.attach(pid)
        except frida.TransportError as e:
            sys.stderr.write(f"{Fore.RED} Got exception {repr(e)} when attaching to {pid}\n{Style.RESET_ALL}")
            return

        session.on('detached',lambda reason: self._reactor.schedule(lambda: self._on_detach(pid, session, reason)))
        session.enable_child_gating() #pause child processes until manually resumed
        for moduleclass in self._base_module.BaseInstrumentation.__subclasses__():
            if moduleclass.modulename in self._loaded_modules: # module might have been unloaded by user
                instrumentation = moduleclass(session, path, self._db)
                self._instrumentations.append(instrumentation)
                instrumentation.load_script()
        print(f"instrumented process with pid: {pid} and path: {path}")
        self._device.resume(pid)
        self._sessions.add(session)

    def _on_detach(self, pid, session, reason):
        """
        Callback called when the Frdia becomes detached froma  process.
        Calls the on_finish method for any loaded instrumentations, removes the old session and prints output, if verbosity is high enough.
        pid: int - PID of detached process
        session: Frida Session object - session corresponded to the detached process
        reason: str - Reason provided by Frida for why the target terminated
        """
        print (f"detached from {pid} for reason {reason}")
        for instrumentation in self._instrumentations:
            instrumentation.on_finish()
        self._instrumentations.clear() #reset for next session, if any
        self._sessions.remove(session)
        verbosity = self.settings_controller.get_setting_int(self.CORE_MODNAME,"verbosity") or 0
        self.export_all(sys.stdout)

        self._reactor.schedule(self._stop_if_idle, delay=0.5)

    def _on_child_added(self, child):
        """
        Callback called by Frida reactor when a new child is spawned from the target process.
        child - object
        """
        self._instrument(child.pid,child.path)

    def _on_child_removed(self,child):
        """
        Callback called by Frida reactor when a child process ends.
        child - object
        """
        print(f"Child removed: {child.pid}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: {0} <target>".format(sys.argv[0]))
        sys.exit(1)
    app = Winstrument()
    if len(sys.argv) >=3:
        args = sys.argv[2]
    else:
        args = None
    app.run(sys.argv[1],args)

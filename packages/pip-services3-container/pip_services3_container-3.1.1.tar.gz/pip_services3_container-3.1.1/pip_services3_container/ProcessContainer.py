# -*- coding: utf-8 -*-
"""
    pip_services3_container.ProcessContainer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Process container implementation.

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import signal
import time
import threading

from pip_services3_components.log import ConsoleLogger
from pip_services3_commons.config import ConfigParams
from .Container import Container


class ProcessContainer(Container):
    """
    Inversion of control (IoC) container that runs as a system process.
    It processes command line arguments and handles unhandled exceptions and Ctrl-C signal
    to gracefully shutdown the container.

    ### Command line arguments ###
        - --config -c             path to JSON or YAML file with container configuration (default: "./config/config.yml")
        - --param --params -p   value(s) to parameterize the container configuration
        - --help -h               prints the container usage help

        Example:
            container = ProcessContainer()
            container.add_factory(MyComponentFactory())

            container.run()
    """
    _config_path = '../config/config.yml'
    _exit_event = None

    def __init__(self, name=None, description=None):
        """
        Creates a new instance of the container.

        :param name: (optional) a container name (accessible via ContextInfo)

        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super(ProcessContainer, self).__init__(name, description)
        self._logger = ConsoleLogger()
        self._exit_event = threading.Event()

    def _get_config_path(self):
        args = sys.argv
        index = 0
        while index < len(args):
            arg = args[index]
            next_arg = args[index + 1] if index < len(args) - 1 else None
            next_arg = None if next_arg != None and next_arg.startswith('-') else next_arg
            if next_arg != None:
                if arg == "--config" or arg == "-c":
                    return next_arg
            index += 1
        return self._config_path

    def _get_parameters(self):
        # Process command line parameters
        args = sys.argv
        line = ''
        index = 0
        while index < len(args):
            arg = args[index]
            next_arg = args[index + 1] if index < len(args) - 1 else None
            next_arg = None if next_arg != None and next_arg.startswith('-') else next_arg
            if next_arg != None:
                if arg == "--param" or arg == "--params" or arg == "-p":
                    if len(line) > 0:
                        line = line + ';'
                    line = line + next_arg
                    index += 1
            index += 1

        parameters = ConfigParams.from_string(line)

        # Process environmental variables
        for (k, v) in os.environ.items():
            parameters[k] = v

        return parameters

    def _show_help(self):
        args = sys.argv
        index = 0
        while index < len(args):
            arg = args[index]
            if arg == "--help" or arg == "-h":
                return True
            index += 1
        return False

    def _print_help(self):
        print("Pip.Services process container - http://www.github.com/pip-services/pip-services")
        print("run [-h] [-c <config file>] [-p <param>=<value>]*")

    def _capture_errors(self, correlation_id):
        def handle_exception(exc_type, exc_value, exc_traceback):
            self._logger.fatal(correlation_id, exc_value, "Process is terminated")
            self._exit_event.set()
            # sys.exit(1)

        sys.excepthook = handle_exception

    def _capture_exit(self, correlation_id):
        self._logger.info(correlation_id, "Press Control-C to stop the microservice...")

        def sigint_handler(signum, frame):
            self._logger.info(correlation_id, "Goodbye!")
            self._exit_event.set()
            # sys.exit(1)

        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)

        # Wait and close
        self._exit_event.clear()
        while not self._exit_event.is_set():
            try:
                self._exit_event.wait(1)
            except:
                pass  # Do nothing...

    def run(self):
        """
        Runs the container by instantiating and running components inside the container.

        It reads the container configuration, creates, configures, references and opens components.
        On process exit it closes, unreferences and destroys components to gracefully shutdown.
        """
        if self._show_help():
            self._print_help()
            return

        correlation_id = self._info.name
        path = self._get_config_path()
        parameters = self._get_parameters()
        self.read_config_from_file(correlation_id, path, parameters)

        self._capture_errors(correlation_id)
        self.open(correlation_id)
        self._capture_exit(correlation_id)
        self.close(correlation_id)

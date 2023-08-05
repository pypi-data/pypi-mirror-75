#!/usr/bin/env python
# coding=utf-8

__author__ = "Garrett Bates"
__copyright__ = "© Copyright 2020, Tartan Solutions, Inc"
__credits__ = ["Garrett Bates, Dave Parsons"]
__license__ = "Apache 2.0"
__version__ = "0.1.2"
__maintainer__ = "Garrett Bates"
__email__ = "garrett.bates@tartansolutions.com"
__status__ = "Development"

import logging
import signal
import os
from collections import namedtuple
from dotenv import load_dotenv
from pathlib import Path

ENV_FILE = Path("/.env")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Debugger(object):
    """Start a debugging session based on environment variables."""

    @staticmethod
    def parse_env():
        load_dotenv(dotenv_path=ENV_FILE, override=True)

        valid_editors = {'vscode', 'pycharm', 'wing'}
        settings = namedtuple('DebugSettings', [
            'enabled',
            'editor',
            'address',
            'port',
            'wait',
        ])
        enabled = os.environ.get('DEBUGGER_ENABLED', 'false').lower() == 'true'
        editor = os.environ.get('DEBUGGER_EDITOR', 'vscode')
        if editor not in valid_editors:
            raise ValueError(f"""DEBUGGER_EDITOR env var has an invalid value of '{editor}' (should be one of {valid_editors}).

                Update your local .env file (located in root of project) and run `devspace run update-env` to resolve this.

                If an .env file does not exist, create one from .env-sample"
            """)
        address = os.environ.get('DEBUGGER_ADDRESS', 'localhost')
        port = 9000 if editor == 'vscode' else 9001
        wait = os.environ.get('DEBUGGER_WAIT', 'false').lower() == 'true'

        debug_settings = settings(
            enabled,
            editor,
            address,
            port,
            wait,
        )
        logger.info(f" Debugger settings:")
        logger.info(f"   enabled: {debug_settings.enabled}")
        logger.info(f"   editor: {debug_settings.editor}")
        logger.info(f"   address: {debug_settings.address}")
        logger.info(f"   port: {debug_settings.port}")
        logger.info(f"   wait: {debug_settings.wait}")
        return debug_settings


    def __init__(self):
        env = Debugger.parse_env()
        self.enabled = env.enabled
        self.editor = env.editor
        self.address = env.address
        self.port = env.port
        self.wait = env.wait


    def start(self):
        # Debugging enabled
        if not self.enabled:
            return

        # Valid IDE configured
        if not self.editor:
            return

        if self.editor == 'vscode':
            import ptvsd
            ptvsd.enable_attach(address=(self.address, self.port), redirect_output=True)
            if self.wait:
                logger.info(" Waiting for debugger to attach...")
                ptvsd.wait_for_attach()

        if self.editor == 'pycharm':
            from contextlib import suppress
            with suppress(ConnectionRefusedError):
                def start_debugger(signum, frame):
                    import pydevd_pycharm
                    logger.info(f" Connecting to debug server on {self.address}...")
                    pydevd_pycharm.settrace(self.address,
                                            port=int(self.port),
                                            stdoutToServer=True,
                                            stderrToServer=True,
                                            suspend=self.wait)

                # Create a custom handler to start debugger, and wait for signal.
                orig_handler = signal.signal(signal.SIGUSR1, start_debugger)
                logger.info(" Waiting to begin debugging session. Start your IDE's debug server and run `devspace run debug` to continue.")
                signal.pause()

                # Set original handler back after handling signal.
                signal.signal(signal.SIGUSR1, orig_handler)
                

        if self.editor == 'wing':
            pass

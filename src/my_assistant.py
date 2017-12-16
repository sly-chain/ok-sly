#!/usr/bin/env python3

"""Run a recognizer using the Google Assistant Library with button support.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import sys
import threading
import subprocess
import RPi.GPIO as GPIO

import aiy.assistant.auth_helpers
import aiy.cloudspeech
import aiy.voicehat
import aiy.audio
import aiy.assistant.grpc
from local_commands.email_commands import EmailAssistant
from local_commands.audio_commands import AudioAssistant

from google.assistant.library import Assistant
from google.assistant.library.event import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


class MyAssistant(object):
    """An assistant that runs in the background.

    The Google Assistant Library event loop blocks the running thread entirely.
    To support the button trigger, we need to run the event loop in a separate
    thread. Otherwise, the on_button_pressed() method will never get a chance to
    be invoked.
    """
    def __init__(self):
        self._task = threading.Thread(target=self._run_task)
        self._can_start_conversation = False
        self._assistant = None

    def start(self):
        """Starts the assistant.

        Starts the assistant event loop and begin processing events.
        """
        self._task.start()

    def _run_task(self):
        credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
        with Assistant(credentials) as assistant:
            self._assistant = assistant
            for event in assistant.start():
                self._process_event(event)


    def _process_event(self, event):
        status_ui = aiy.voicehat.get_status_ui()
        button = aiy.voicehat.get_button()
        
        if event.type == EventType.ON_START_FINISHED:
            status_ui.status('ready')
            self._can_start_conversation = True
            # Start the voicehat button trigger.
            button.on_press(self._on_button_pressed)
            
            if sys.stdout.isatty():
                print('Say "OK, Google" or press the button, then speak. '
                      'Press Ctrl+C to quit...')

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self._can_start_conversation = False
            status_ui.status('listening')

        elif event.type == EventType.ON_END_OF_UTTERANCE:
            status_ui.status('thinking')
            
        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            print('You said:', event.args['text'])
            text = event.args['text'].lower()

            #audio commands
#            if text == 'record me':
#                self._assistant.stop_conversation()
#                AudioAssistant._record_file()
            
            #led commands
            if text == 'LED mode':
                self._assistant.stop_conversation()
                try:
                    self._led_control()
                except:
                    self._destroy_GPIO()
            
            #email commands
            if text == 'send emails':
                self._assistant.stop_conversation()
                EmailAssistant._send_files()
            
            
            #power commands
#            elif text == 'shutdown':
#                self._assistant.stop_conversation()
#                self._shutdown()
#            elif text == 'reboot':
#                self._assistant.stop_conversation()
#                self._reboot_pi()
            

        elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
            status_ui.status('ready')
            self._can_start_conversation = True

        elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
            sys.exit(1)
            

    def _on_button_pressed(self):
        # Check if we can start a conversation. 'self._can_start_conversation'
        # is False when either:
        # 1. The assistant library is not yet ready; OR
        # 2. The assistant library is already in a conversation.
        if self._can_start_conversation:
            self._assistant.start_conversation()
    
    

    

def main():
    MyAssistant().start()


if __name__ == '__main__':
    main()
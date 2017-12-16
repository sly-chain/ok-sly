#!/usr/bin/env python3

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

# reason this doesn't work ... it's hotword trigger before running
# the recongize function.
# then it records whatever and sends it to the google assistant API

def recognize_hotwords():
    recognizer = aiy.cloudspeech.get_recognzier()
    recognizer.expect_hotword(['hey cunt face', 'google'])
    recognizer.recognize()    

def _hotword_detection(self, event):
    recognizer = aiy.cloudspeech.get_recognzier()
    recognizer.expect_phrase('hey cunt face')
    
    while True:
        print('Listening')
        text = recognizer.recognize()
        print('You said "', text, '"')
        if 'hey cunt face' in text:
            self._assistant.start_conversation()


# records, listening for the hotword.
# but times out if nothing is said after a while. 
            
def _custom_hotwords_uttered(self, event):
    assistant = aiy.assistant.grpc.get_assistant()
    # need to add this with statement, otherwise recorder won't start
    # start() method seems deprecated. can't find it anywhere.

    with aiy.audio.get_recorder():
        while True:
            print('Listening...')
            text, audio = assistant.recognize()
            print('You said "', text, '"')
            if text is not None:
                if 'hey cunt face' in text and self._can_start_conversation:
                    self._assistant.start_conversation()
            else:
                self._assistant.start()
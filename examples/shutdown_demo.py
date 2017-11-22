#!/usr/bin/env python3

import aiy.audio
import aiy.cloudsppech
import aiy.voicehat
import subprocess

def shutdown():
    shut_down_list = ['shutdown', 'good bye', 'power off', 'turn off']
    recognizer = aiy.cloudspeech.get_recognzier()
    recognizer.expect_phrase(shut_down_list)
    
    button = aiy.voicehat.get_button()
    aiy.audio.get_recorder().start()
    
    while True:
        print('Pressthe button and speak')
        button.wait_for_press()
        print('Listening ...')
        
        text = recognizer.recognize()
        
        if text is None:
            print('Sorry I didn\'t hear you')
        else: 
            print('You said "', text, '"')
            if text in shut_down_list:
                subprocess.call(['sudo', 'shutdown', '-h', 'now'])

        
#!/usr/bin/env python3

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import RPi.GPIO as GPIO

def main():
    recognizer = aiy.cloudspeech.get_recogniser()
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('turn off the light')
    
    button = aiy.voicehat.get_button()
    aiy.audio.get_recorder().start()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)
    
    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening ...')
        text = recognizer.recognize()
        if text is None:
            print('Sorry, I did not hear you')
        else:
            print('You said "', text, '"')
            if 'turn on the light' in text:
                GPIO.output(26, GPIO.HIGH)
            elif 'turn off the light' in text:
                GPIO.output(26, GPIO.LOW)

if __name__ == '__main__':
    main()
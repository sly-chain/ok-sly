#!/usr/bin/env python3

import aiy.audio 
import aiy.cloudspeech
import aiy.voicehat


def detect_motion():
    my_motion_detector = MotionDetector()
    recognizer = aiy.cloudspeech.get_recognizer()
    aiy.audio.get_recorder().start()
    
    while True:
        my_motion_detector.WaitForMotion()
        text = recognizer.recognize()
        aiy.audio.say('You said ', text)


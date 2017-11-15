import aiy.audio
import aiy.cloudsppech
import aiy.voicehat
import subprocess

def shutdown():
    shut_down_list = ['shutdown', 'good bye', 'power off', 'turn off']
    recognizer = aiy.cloudspeech.get_recognzier()
    recognizer.expect_phrase(shut_down_list)
    
    while True:
        text = recognizer.recognize()
        print('You said "', text, '"')
        if text in shut_down_list:
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])

        
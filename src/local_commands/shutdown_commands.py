#!/usr/bin/env python3

import subprocess
import RPi.GPIO as GPIO

import aiy.assistant.auth_helpers
import aiy.cloudspeech
import aiy.voicehat
import aiy.audio
import aiy.assistant.grpc


#local commands - power
def _destroy_GPIO(self):
    GPIO.output(26, GPIO.LOW)
    GPIO.cleanup()
    
def _shutdown(self):
    print('shut down')
    aiy.audio.say('Turning Off')
    self._destroy_GPIO()
    subprocess.call(['sudo', 'shutdown', '-h', 'now'])

def _reboot(self):
    print('reboot')
    aiy.audio.say('Restarting')
    self._destroy_GPIO()
    subprocess.call(['sudo', 'reboot', '-h', 'now'])
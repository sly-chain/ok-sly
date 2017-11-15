#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import src.aiy.audio
import src.aiy.cloudspeech
import src.aiy.voicehat


def main():
    recognizer = src.aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = src.aiy.voicehat.get_button()
    led = src.aiy.voicehat.get_led()
    src.aiy.audio.get_recorder().start()

    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        if not text:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            if 'turn on the light' in text:
                led.set_state(src.aiy.voicehat.LED.ON)
            elif 'turn off the light' in text:
                led.set_state(src.aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(src.aiy.voicehat.LED.BLINK)
            elif 'goodbye' in text:
                break


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

from gtts import gTTS
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    wav_file = tts.save('audio.wav')
    
    return wav_file

#speak('Hi, what can I do for you?')
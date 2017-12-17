#!/usr/bin/env python3

#import os
#import sys
import wave

import aiy.audio
import aiy.cloudspeech

#sys.path.append(os.path.realpath(os.path.join(__file__, '..', '..')) + '/src/')


class AudioAssistant():
    
    def __init__(self):
        self._wav_file = 'my_recording.wav'
    
    #local commands - create and save file
    def _create_wav_file(self):
        wave_file = wave.open(self._wav_file, 'wb')
    
        try:
            aiy.audio.say('recording')
            print('Recording ...')
            aiy.audio.record_to_wave(wave_file, 5)
            wave_file.setnchannels(2)
            wave_file.setsampwidth(2)
            wave_file.setframerate(44100)
            
        except:
            aiy.audio.say('i did not get that')
            print('Problems with recording')
            
        finally:
            wave_file.close()
    
    
    def _play_wav_file(self):
        try:
            aiy.audio.play_wave(self._wav_file)
        except FileNotFoundError:
            print('file not found')
            pass


#def main():
    #AudioAssistant._create_wav_file()

#if __name__ == '__main__':
    #main()


    #local commands - repeat
    #built in already. don't need it. 
# =============================================================================
#     def repeat_after_me():
#         assistant = aiy.assistant.grpc.get_assistant()
#         with aiy.audio.get_recorder():
#             while True:
#                 print('Listening ...')
#                 text, audio = assistant.recognize()
#                 if text is not None:
#                     print('You said, "', text, '"')
#                     aiy.audio.say(text)
#                 else:
#                     print('I did not hear you')
#     
#     def delete_file(wave_file):
#         try:
#             print('deleting file ...')
#         except FileNotFoundError:
#             pass 
# =============================================================================

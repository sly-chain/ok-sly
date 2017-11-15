import aiy.audio
import aiy.cloudsppech
import aiy.voicehat


def recognize_hotwords():
    recognizer = aiy.cloudspeech.get_recognzier()
    recognizer.expect_hotword(['hey cunt face', 'google'])
    recognizer.recognize()    


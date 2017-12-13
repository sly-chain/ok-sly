import aiy.audio
import aiy.cloudsppech
import aiy.voicehat


def recognize_hotwords():
    recognizer = aiy.cloudspeech.get_recognzier()
    recognizer.expect_hotword(['cunt face', 'fucker'])
    recognizer.recognize()    


    with aiy.audio.get_recorder():
        while True:
            text = recognizer.recognize()
            if text is not None:
                print('You said "', text, '"')
            else:
                print('Sorry, I did not hear you')

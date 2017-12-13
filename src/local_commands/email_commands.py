import smtplib
import sys
print(sys.path)
import os

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from src.my_assistant import MyAssistant
import aiy.audio
import aiy.voicehat

from google.assistant.library.event import EventType


class EmailAssistant(MyAssistant):
    
    def __init__(self):
        MyAssistant.__init__(self)
    
    def _process_event(self, event):
        status_ui = aiy.voicehat.get_status_ui()
        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            print('You said:', event.args['text'])
            text = event.args['text'].lower()
            
            if text == 'email attachment':
                assistant = aiy.assistant.grpc.get_assistant()
                with aiy.audio.get_recorder():
                    while True:
                        aiy.audio.say('who should i send the email to')
                        print('Listening ...')
                        text, audio = assistant.recognize()
                        if text is not None:
                            print('You said, "', text, '"')
                            text = recipient
                        else:
                            aiy.audio.say('i did not understand you, would you like to continue')
                            print('I did not hear you')
                            text, audio = assistant.recognize()
                            if text == 'yes':
                                self._process_event()
                            else: 
                                aiy.audio.say('ok')
                                status_ui.status('ready')
                                self._can_start_conversation = True
                
                
                self._send_attachment(recipient, 
                    'Subject', 
                    'Dear sir..', 
                    ['tkinter_gui.py'])


    def _send_attachment(self, recipient, subject, body, files=[]):
        assert type(recipient)==list
        assert type(files)==list
    
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = COMMASPACE.join(recipient)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
    
        msg.attach(MIMEText(body))
    
        for file in files:
            try:
                part = MIMEBase('application', "octet-stream")
                with open(file, 'rb') as fp:
                    part.set_payload(fp.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                msg.attach(part)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise
    
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(user, passwd)
                s.sendmail(user, recipient, msg.as_string())
                s.close()
            print("Email sent!")
            s.quit()
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise
    
    

user = ''
passwd = ''

#send_attachment( [recipient], subject, body, [attach] )
EmailAssistant._send_attachment(['@gmail.com'], 
         'Subject', 
         'Dear sir..', 
         ['tkinter_gui.py'])


def main():
    EmailAssistant._send_attachment()(['@gmail.com'], 
         'Subject', 
         'Dear sir..', 
         ['tkinter_gui.py'] )

if __name__ == '__main__':
    main()
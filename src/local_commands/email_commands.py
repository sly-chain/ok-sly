import smtplib
import sys
print(sys.path)
import os

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
#from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from src.my_assistant import MyAssistant
import src.aiy.audio
import src.aiy.voicehat


class EmailAssistant(MyAssistant):
    
    def __init__(self):
        MyAssistant.__init__(self)
    
    def _confirm_response(self, phrase, response, function):
        assistant = src.aiy.assistant.grpc.get_assistant()
        
        src.aiy.audio.say('is this correct?')
        text, audio = assistant.recognize()
        
        if text == 'yes':
            src.aiy.audio.say(phrase, response)
            return response
        elif text == 'no':
            self._try_again(function)
    
    def _confirm_information(self):
        status_ui = src.aiy.voicehat.get_status_ui()
        recipient = self._set_recipient()
        file_name = self._set_attachment()
        files = file_name + '.wav'
        
        src.aiy.audio.say('let\'s confirm. you would like', file_name, 'sent to', recipient, 'is this correct?')
        assistant = src.aiy.assistant.grpc.get_assistant()
        text, audio = assistant.recognize()
        
        if text == 'yes':
            src.aiy.audio.say('ok sending email')
            self._send_files(recipient, files)
        elif text == 'no':
            src.aiy.audio.say('ok')
            status_ui.status('ready')
            self._can_start_conversation = True  
    
    
    def _try_again(self, function):
        status_ui = src.aiy.voicehat.get_status_ui()
        assistant = src.aiy.assistant.grpc.get_assistant()
        
        src.aiy.audio.say('would you like to try again?')
        text, audio = assistant.recognize()
        
        if text == 'yes':
            function()
        else: 
            src.aiy.audio.say('ok')
            status_ui.status('ready')
            self._can_start_conversation = True
    
    def _set_recipient(self):
        assistant = src.aiy.assistant.grpc.get_assistant()
        
        src.aiy.audio.say('who should i send the email to')
        print('Listening ...')
        text, audio = assistant.recognize()
        
        if text is not None:
            src.aiy.audio.say('You said', text)
            print('You said, "', text, '"')
            self._confirm_response('ok email will be sent to', text, self._set_recipient)

        else:
            print('i did not hear you')
            src.aiy.audio.say('i did not hear you')
            self.try_again(self._set_recipient)
    
    
    def _set_files(self):
        assistant = src.aiy.assistant.grpc.get_assistant()
        
        src.aiy.audio.say('what file should i send?')
        print('Listening ...')
        text, audio = assistant.recognize()
        
        if text is not None:
            print('You said, "', text, '"')
            src.aiy.audio.say('you said', text, 'is this correct?')
            
            self._confirm_response('ok email will be sent to', text, self._set_files)
            
            
            file_name = text
            return file_name
        else:
            print('i did not hear you')
            src.aiy.audio.say('i did not hear you')
            self._try_again(self._set_attachment)      



    def _send_files(self, recipient, files=[]):
        assert type(recipient)==list
        assert type(files)==list
    
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = COMMASPACE.join(recipient)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'files from the cardboard'
    
#        msg.attach(MIMEText(body))
    
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
        
        finally:
            recipient = []
            files = []
    

user = ''
passwd = ''

#send_attachment( [recipient], subject, body, [attach] )
EmailAssistant._send_files(['@gmail.com'], 
         'Dear sir..', 
         ['tkinter_gui.py'])


def main():
    EmailAssistant._files()(['@gmail.com'], 
         'Dear sir..', 
         ['tkinter_gui.py'] )

if __name__ == '__main__':
    main()
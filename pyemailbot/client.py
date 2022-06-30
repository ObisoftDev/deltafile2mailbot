import smtplib, ssl
import imaplib
from os.path import basename
import email
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.utils import COMMASPACE, formatdate
from .threads import DispatchThread
from email import encoders


class EmailBot(object):
    def __init__(self, email='user@nauta.cu',email_password='xxx',type='nauta'):
        self.imapssl = False

        self.type = type

        if type=='nauta':
            self.smtp_host_server = 'smtp.nauta.cu'
            self.smtp_port = 25
            self.imap_host_server = 'imap.nauta.cu'
            self.imap_port = 143

        if type=='gmail':
            self.smtp_host_server = 'smtp.gmail.com'
            self.smtp_port = 587
            self.imap_host_server = 'imap.gmail.com'
            self.imap_port = 993
            self.imapssl = True

        if type=='yahoo':
            self.smtp_host_server = 'smtp.mail.yahoo.com'
            self.smtp_port = 587
            self.imap_host_server = 'imap.mail.yahoo.com'
            self.imap_port = 993
            self.imapssl = True

        self.email = email
        self.email_password = email_password
        self.smtp_server = None
        self.imap_server = None
        self.dispatching = False
        self.context = ssl.create_default_context()

    def login(self):
        try:
            self.smtp_server = smtplib.SMTP(self.smtp_host_server,self.smtp_port)
            if self.type=='gmail':
               self.smtp_server.starttls()
            if self.imapssl:
                self.imap_server = imaplib.IMAP4_SSL(self.imap_host_server,self.imap_port)
            else:
                self.imap_server = imaplib.IMAP4(self.imap_host_server,self.imap_port)
            self.smtp_server.login(self.email, self.email_password)
            self.imap_server.login(self.email, self.email_password)
        except Exception as ex:
            print(str(ex))
            return False
        return True

    def logout(self):
        try:
            self.smtp_server.quit()
            self.imap_server.close()
            self.imap_server.logout()
        except:return False
        return True

    def send_mail(self,to_email=[],subject='SMTPNat Use Python Lib',message='Message Here!',files=[]):
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = ', '.join(to_email)
            msg.attach(MIMEText(message))
            for f in files or []:
                with open(f, "rb") as fil:
                    if 'zip' in f or '7z' in f or 'rar' in f or 'exe' in f or 'apk' in f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(fil.read())
                        encoders.encode_base64(part)
                    elif '.png' in f or '.jpg' in f:
                        part = MIMEImage(fil.read())
                        encoders.encode_base64(part)
                    elif '.mp3' in f or '.ogg' in f or '.wav' in f:
                        part = MIMEAudio(fil.read())
                        encoders.encode_base64(part)
                    else:
                        part = MIMEApplication(
                            fil.read(),
                            Name=basename(f)
                        )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)
            data = self.smtp_server.send_message(msg)
            return msg

    def dispatch_receiv_emails(self,onenteremail=None):
        self.dispatching = True
        while self.dispatching:
            try:
                self.imap_server.select('inbox')
                status, data = self.imap_server.search(None, '(UNSEEN)')
                mail_ids = []
                for block in data:
                    mail_ids += block.split()
                for i in mail_ids:
                    status, data = self.imap_server.fetch(i, '(RFC822)')
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            message = email.message_from_bytes(response_part[1])
                            if onenteremail:
                                thread = DispatchThread(onenteremail,args=(self,EmailMessage(self,message)))
                                thread.start()
            except Exception as ex:
                print(str(ex))
                self.logout()
                self.dispatching = self.login()

class EmailMessage (object):
      def __init__(self,natemail,message):
          self.message = message
          self.natemail = natemail
          self.mail_from = self._parse_email_from(message['from'])
          self.mail_subject = message['subject']
          self.mail_me = natemail.email
          self.mail_content = self._to_content()

      def _parse_email_from(self,data):
          return str(data).split('<')[1].replace('>','')

      def _to_content(self):
          main_content = ''
          if self.message.is_multipart():
             for part in self.message.get_payload():
                 main_content += part.get_payload()
          else:
               main_content = self.message.get_payload()
          return self._parse_content(main_content)

      def _parse_content(self,content):
          return str(content).split('\r\n\r\n--')[0]

      def reply_text(self,text,subject='Reply Text'):
          return self.natemail.send_mail(to_email=[self.mail_from],subject=subject,message=text)

      def reply_file(self,file,text='Reply File',subject='Reply File'):
          return self.natemail.send_mail(to_email=[self.mail_from],subject=subject,message=text,files=[file])

      def reply_files(self,files=[],text='Reply File',subject='Reply File'):
          return self.natemail.send_mail(to_email=[self.mail_from],subject=subject,message=text,files=files)

      def __str__(self):return str(self.message)
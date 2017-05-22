import imaplib,smtplib,re,time
from email.mime.multipart import MIMEMultipart
from sys import platform
from email.mime.text import MIMEText
class Mailbot:


    def __init__(self,username,password,host='imap.gmail.com'):
        self.imap=imaplib.IMAP4_SSL(host)
        self.username=username
        self.password=password
        self.host=host
        try:
            self.imap.login(username,password)
            print('Login successful')
        except  Exception  as e:
            print('Login Failed '+str(e))
            exit(1)


    def logout(self):
        try:
            self.imap.logout()
            print('Logout Successful')
        except:
            print('Unable to logout')


    def count_unread_mails(self,folder='inbox'):
        try:
            return  str(self.imap.status(folder,"(UNSEEN)")[1]).split(' ')[2].strip(")']")
        except Exception as e:
            print('Unable to fetch '+str(e))
            exit(1)


    def send_mail(self,toaddr,message,subject):
        try:
            temp_smtp=smtplib.SMTP(self.host,port=587)
            temp_smtp.starttls()
            temp_smtp.login(self.username,self.password)
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['Subject'] = subject
            body = message
            msg.attach(MIMEText(body, 'plain'))
            msg['To'] = toaddr
            text=msg.as_string()
            temp_smtp.sendmail(self.username, toaddr,text)
            print('Successfully sent')
            temp_smtp.quit()
        except Exception as e:
            print('Unable to send '+ str(e))
            self.imap.logout()
            exit(1)


    def get_subject(self,raw_mail):
        import email
        email_message = email.message_from_bytes(raw_mail)
        try:
            return str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
        except:
            print('unable to get header')
            exit(1)

    def fetch_mail(self,raw_email):
        import email
        email_message = email.message_from_bytes(raw_email)
        print('From : '+str(email.utils.parseaddr(email_message['From'])))
        hdr = email.header.make_header(email.header.decode_header(email_message['Subject']))
        subject = str(hdr)
        print('Subject : '+subject)
        print('Body Text : ')
        maintype = email_message.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message.get_payload():
                if part.get_content_maintype() == 'text':
                    print(part.get_payload())
        elif maintype == 'text':
            print(email_message.get_payload())
        try:
            if platform == "linux" or platform == "linux2":
                import  os
                os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 200))
            elif platform == "win32":
                 import winsound
                 winsound.Beep(300, 2000)
        except Exception as e:
            print(str(e))

    def current_mails(self):
        return int(str(self.imap.select('inbox')).split("'")[3])


    def attach_to_mail(self,regular_expression=None,timeout=None):

        try:
            if timeout==None:
                temp=self.current_mails()
                time.sleep(2)
                while 1:
                    data=self.current_mails()
                    if data>temp:
                        for i in range(0,data-temp):
                            typ,temp_data=self.imap.fetch(bytes(str(data-i),'utf-8'),'(RFC822)' )
                            if regular_expression==None:
                                self.fetch_mail(temp_data[0][1])
                            else:
                                r=re.compile(regular_expression)
                                if len(r.findall(self.get_subject(temp_data[0][1])))!=0:
                                    self.fetch_mail(temp_data[0][1])
                        temp = data
                    time.sleep(2)
        except Exception as e:
            self.imap.logout()
            print('Failed \n'+str(e))
            exit(1)
        else:
            try:
                temp_ticks=int(time.time())
                final_ticks=temp_ticks+timeout
                while temp_ticks<final_ticks:
                    temp_ticks=int(time.time())
                    temp_1=self.current_mails()
                    time.sleep(2)
                    data_timeout=self.current_mails()
                    if data_timeout>temp_1:
                        for i in range(0,data_timeout-temp_1):
                            typ, temp_data = self.imap.fetch(bytes(str(data_timeout-i),'utf-8'), '(RFC822)')
                            if regular_expression == None:
                                self.fetch_mail(temp_data[0][1])
                            else:
                                r=re.compile(regular_expression)
                                if len(r.findall(self.get_subject(temp_data[0][1]))) != 0:
                                    self.fetch_mail(temp_data[0][1])
                    temp_1=data_timeout
                    time.sleep(2)
                    temp_ticks=int(time.time())
                self.imap.logout()
            except Exception as e:
                self.imap.logout()
                print(str(e))
                exit(1)

    def detach(self):
        try:
            self.imap.logout()
        except Exception as e:
            print(str(e))

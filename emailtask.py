from email import header
from platform import machine
import re
import imaplib
import email, email.parser
import smtplib
import os 
import re

def emailtasl():
    imap = imaplib.IMAP4_SSL('outlook.office365.com')
    imap.login('youremail@outlook.com', 'password') 
    imap.select('Inbox')
    _, search_data = imap.search(None, 'ALL')
    for num in search_data[0].split():
        _, data = imap.fetch(num, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        # print(email_message)
        for header in ['subject','to','from','date']:
            # print("{}: {}".format(header,email_message[header]))
            print("------")
        for part in email_message.walk():
            if part.get_content_type() == "text/plain" or part.get_content_type == "text/html":
                body = part.get_payload(decode=True)
                email_data = body.decode()
                print(email_data)
                # print(email_message)
                # # print('===================================================================')
                # print(email_message)
                from_addr = email_message.get("From")
                # print(from_addr)
                subject = email_message.get("subject")
                print(subject)
                message_id = email_message.get("Message-ID")
                # print(message_id)
                received = email_message.get("Received")
                # print(received)
                if 'rupeshsc1999@outlook.com' in from_addr:
                    toaddr = 'a.singh.act@outlook.com'
                    fromaddr = "as098765432@outlook.com"
                    mss = "Escalation Mail.Please Look into it ASAP"
                    alll = mss#+' '+email_data
                    message_text = email.message_from_string(alll)
                    message = message_text
                    smtp = smtplib.SMTP('smtp.office365.com', 587)
                    smtp.starttls()
                    smtp.login('as098765432@outlook.com','Pass')
                    smtp.sendmail(fromaddr, toaddr, message.as_string())
                    print("Forward Mails Sent successfully")
                    smtp.quit()
                if 'a.singh.act@outlook.com' in from_addr:
                    server =imaplib.IMAP4_SSL('outlook.office365.com',993)
                    server.login('as098765432@outlook.com','Pass')
                    server.select()
                    typ, data = server.search(None, '(SUBJECT "")')
                    mail_ids = data[0]
                    id_list = mail_ids.split()
                    path = r"C:\Users\As\Desktop\Sequalstring\Emailtask"
                    for num in data[0].split():
                        typ, data = imap.fetch(num, '(RFC822)' )
                        raw_email = data[0][1]
                        raw_email_string = raw_email.decode('utf-8')
                        email_message = email.message_from_string(raw_email_string)
                        for part in email_message.walk():
                            # if part.get_content_maintype() == 'multipart':
                            #     continue
                            # if part.get('Content-Disposition') is None:
                            #     continue
                            fileName = part.get_filename()
                            if bool(fileName):
                                if 'image' in fileName or 'IMG' in fileName:
                                    pass
                                elif fileName.endswith('.xlsx') or fileName.endswith('.csv'):
                                    filePath = os.path.join(path, fileName)
                                    if not os.path.isfile(filePath) :
                                        fp = open(filePath, 'wb')
                                        # fp.write(part.get_payload(decode=True))
                                        fp.close()
                                    aps = smtplib.SMTP('smtp.office365.com', 587)
                                    aps.starttls()
                                    em_mssg = "Your Mail has been received and all the necessary docs have been downloaded"
                                    massg = email.message_from_string(em_mssg,)
                                    massage = massg
                                    aps.login('as098765432@outlook.com','Pass')
                                    aps.sendmail('as098765432@outlook.com','a.singh.act@outlook.com', massage.as_string())
                                    print("Reply Send")
                    server.logout
                    print("Attachment downloaded from mail")
                else:
                    if 'rupeshsc1999@outlook.com' not in from_addr and 'a.singh.act@outlook.com' not in from_addr:
                        if subject == 'RPA':
                            toaddr = 'kj@outlook.com'
                            fromaddr = "as098765432@outlook.com"
                            mssges = "This mail is related to    RPA"
                            email_dat = mssges#+' '+email_data
                            message_text = email.message_from_string(email_dat)
                            message1 = message_text
                            smtp = smtplib.SMTP('smtp.office365.com', 587)
                            smtp.starttls()
                            smtp.login('as098765432@outlook.com','pass')
                            smtp.sendmail(fromaddr, toaddr, message1.as_string())
                            print("RPA Mails Sent successfully")
                            smtp.quit()
                        if subject == 'Data Science' or subject == 'Artificial Intelligence' or subject == 'Machine learning':
                            toaddr = 'apeane@outlook.com'
                            fromaddr = "as098765432@outlook.com"
                            mssges = "This mail is related to Analytics/AI"
                            email_da = mssges#+' '+email_data
                            message_text = email.message_from_string(email_da)
                            message2 = message_text
                            smtp = smtplib.SMTP('smtp.office365.com', 587)
                            smtp.starttls()
                            smtp.login('as098765432@outlook.com','Pass')
                            smtp.sendmail(fromaddr, toaddr, message2.as_string())
                            print("AI and ML Mails Sent successfully")
                            smtp.quit()
                        else:
                            pass
emailtasl()

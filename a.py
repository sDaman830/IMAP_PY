import imaplib
import base64
import os
import email
email_user = input('Email: ')
email_pass = input('Password: ')
import ssl

context = ssl.create_default_context()
context.set_ciphers('DEFAULT:!DH')
mail = imaplib.IMAP4_SSL("imap.qlc.co.in", 993, ssl_context=context)
mail.login(email_user, email_pass)
mail.select()

type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(fileName) 
            if not os.path.isfile(filePath):
                with open(filePath, 'wb') as fp:
                    fp.write(part.get_payload(decode=True))

            subject = email_message['Subject']
            print('Downloaded "{file}" from email titled "{subject}".'.format(file=fileName, subject=subject))

mail.close()
mail.logout()

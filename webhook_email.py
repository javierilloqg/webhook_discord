#!/usr/bin/env python

"""
In this code I will use Discord's webhooks to send data received into a Gmail account.
For this to run, the script must be running constantly and generate an alternative password
for the Gmail account to be scraped. You MUST change the information stored in the variables
marked with grenn # in order to succesfully connect to your Gmail account and get the email 
data.

- Part of the code based in the following tutorial:
https://www.techgeekbuzz.com/how-to-read-emails-in-python/

"""

import email
import imaplib
import time
import re
from dhooks import Webhook
from datetime import datetime

#### CHANGE THIS LINES ACCORDING TO YOUR APP PASSWORD AND EMAIL ####
username = ''
app_password = ''
scraped_email = ''
discord_url = ''
###################################################################

host = 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(host, 993)
mail.login(username, app_password)

try:
    while True:

        # Select INBOX as main folder to check
        mail.select('INBOX')
        # Select only emails marked as unseen from the specified email address
        _, selected_emails = mail.search(None, '(UNSEEN)', f'(FROM "{scraped_email}")')
        print("[" + str(datetime.now()) + "] " + "Unseen emails from selected address: ", \
            len(selected_emails[0].split()))

        for num in selected_emails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            # Byte data to message
            email_message = email.message_from_bytes(bytes_data)
            print("\n===========================================")
            # Access email data
            print("Subject: ",email_message["subject"])
            print("From: ",email_message["from"])
            for part in email_message.walk():
                if part.get_content_type()=="text/plain":
                    message = part.get_payload(decode=True)
                    #print("Message: \n", str(message.decode())[0:-700])
                    mensaje = re.sub(r"http\S+", "", str(message.decode())[737:]).strip()
                    print((mensaje.replace('<','')[:-4136].strip()))
                    print("==========================================\n")
                    break
            hook = Webhook(discord_url)
            mensaje_hook = str(mensaje.replace('<','')[:-4136]).strip()
            hook.send("**" + mensaje_hook.replace('\n', '') + "**")
        time.sleep(0.5)

except KeyboardInterrupt:
    mail.logout()
    print("Script stopped and logged out")

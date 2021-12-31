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
from dhooks import Webhook
from datetime import datetime

#### CHANGE THIS LINES ACCORDING TO YOUR APP PASSWORD AND EMAIL #### 
username = 'javiquesadagalban@gmail.com'
contraseña_aplicacion = 'fgxs ypcp yyjf jrmn'
discord_url = 'https://discord.com/api/webhooks/926152804765151252/L85Z-xUzBy-sbet6uJRzc3pYZ_n8TM2pKQ8z6Nobsn006zzBfZgReklaiemF3OKgtczZ'
###################################################################

host = 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(host, 993)
mail.login(username, contraseña_aplicacion)

while True:

    # Select INBOX as main folder to check
    mail.select('INBOX')
    # Select only emails marked as unseen from the specified email address
    _, selected_emails = mail.search(None, '(UNSEEN)', '(FROM "javiquesadagalban@gmail.com")')
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
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                print("Message: \n", str(message.decode())[0:100])
                print("==========================================\n")
                break
        hook = Webhook(discord_url)
        hook.send(str(message.decode())[0:100])
    time.sleep(0.5)



""" """
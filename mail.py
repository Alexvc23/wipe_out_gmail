import imapclient
import pprint as p
import pyzmail
import re

#Connecting to gmail server
imapObj = imapclient.IMAPClient('imap.gmail.com',ssl=True)
#logging into gmail account
imapObj.login('alexandervalencia1994@gmail.com','C4n4d42309')

# list of mails we want to delete
list_mail = ['FROM', 'linkedin', 'FROM', 'flyingblue', \
    'FROM', 'laposte','FROM', 'duolingo','FROM','hillsong',\
    'FROM', 'lapartdieu', 'FROM','yuka', 'FROM','google', \
    'FROM', 'redditmail', 'FROM', 'fun-mooc', 'FROM', 'notion',\
    'FROM', 'stackoverflow', 'FROM', 'fizzup', 'FROM', 'bm-lyon', \
    'FROM', 'hello.platzi', 'FROM', 'leboncoin', 'FROM', 'youversion',\
    'FROM', 'wordpress', 'FROM', 'skillshare', 'FROM', 'lifemiles', 'FROM', 'login@42.fr']

# length of OR we want to add to our arguments
_len = int((len(list_mail) - 2) / 2)
# we append all the OR strings
for i in range(_len):
    list_mail.insert(0, 'OR')

""" #print list of folder
p.pprint(imapObj.list_folders()) """

#select folder containing all emails
imapObj.select_folder('INBOX', readonly=False)
#search for undesirable emails with serch method
UIDs=imapObj.search(list_mail)
#print ids presenting each mail
print(UIDs)
"""     # ─── SHOW MESSAGES AND SUBJECTS ─────────────────────────────────────────────────
for i in UIDs:
    #extract all iformation into special format
    rawMessages = imapObj.fetch([i], ['BODY[]'])
    msg = pyzmail.PyzMessage.factory(rawMessages[i][b'BODY[]'])

    #print email content
    # msg.html_part.get_payload().decode(msg.html_part.charset)

    #print subject
    print(msg.get_subject()) """
imapObj.delete_messages(UIDs)
imapObj.expunge()
 # ─── DELETE MESSAGES FROM FORLDER BIN AND SPAM ──────────────────────────────────
folders = ["[Gmail]/Spam", "[Gmail]/Bin"]
for i in folders:
    imapObj.select_folder(i, readonly=False)
    UIDs = imapObj.search(['ALL'])
    imapObj.delete_messages(UIDs)
    imapObj.expunge()
imapObj.logout()
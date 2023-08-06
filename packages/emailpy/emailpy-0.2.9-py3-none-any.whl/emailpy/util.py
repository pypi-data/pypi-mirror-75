from .send import genzoominvite
from .read import EmailMessage, EmailMessageList
from .servers import getserver
from .sort import sort

import smtplib
import imaplib

import email as _email
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import os
import re
import threading

from base64 import *

from ospy import basename

class EmailSender:
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = b85encode(pwd.encode())
        self.conn, self.tls = getserver(email, 'smtp')
        self.conn.ehlo()
        if self.tls:
            self.conn.starttls()
        self.conn.login(email, pwd)

    def send(self, toemails, subject = '', body = '', html = None,
             attachments = None, nofileattach = None):
        
##        return sendmail(self.email, b85decode(self.pwd).decode(),
##                        toemails, subject, body, html,
##                        attachments, nofileattach)
        if type(toemails) == str:
            toemails = [toemails]
        if type(attachments) == str:
            attachments = [attachments]
        if not html:
            html = ''

        attachments = attachments or []
        nofileattach = nofileattach or {}
        
        for x in attachments:
            nofileattach[x] = open(x, 'rb').read() # create nofileattach dictionary
        for filename, filedata in nofileattach.items():
            if type(filedata) == str:
                nofileattach[filename] = filedata.encode()

        # background function
        def _sendmail(self, pwd, toemails, subject, body, \
                      html, attachments, nofileattach, mail):
            # generate the email
            msg = MIMEMultipart('alternative') # create base multipart
            msg['From'] = self.email # set fromemail
            msg['To'] = ', '.join(toemails) # set toemails
            msg['Date'] = formatdate(localtime = True) # set date using formatdate
            msg['Subject'] = subject # set subject

            # convert body text to html and add html to end. 
            html = '<pre style = "font-family: Calibri;">'+body+'</pre>'+html
            msg.attach(MIMEText(html, 'html')) # add html and body to email

            for file in nofileattach: # iter through attachments to add to email
                part = MIMEApplication(nofileattach[file], Name = basename(file))
                part['Content-Disposition'] = 'attachment; filename="%s"'\
                                              %basename(file)
                msg.attach(part) # add attachment to email
                
            self.conn.sendmail(self.email, toemails, str(msg)) # send email

            mail.sent = True # set mail.sent variable to True (set remotely)

    ##    mail = EmailMessage2(fromemail, toemails, subject, body,
    ##                         html, nofileattach) # create mail object
        mail = EmailMessage((self.email, (subject, body, html,
                                        [{os.path.basename(x): \
                                          b64encode(y).decode()} for x, y in \
                                         nofileattach.items()],
                                         formatdate(localtime = True)),
                             toemails, None), self.email, '',
                            sendobj = True)

        _sendmail_thread = threading.Thread(target = _sendmail, args = (
            self, b85decode(self.pwd).decode(), toemails, subject,
            body, html, attachments, nofileattach, mail)) # create background thread
        _sendmail_thread.daemon = True # set daemon to True (to run in the background)
        _sendmail_thread.start() # start the thread

        return mail # return mail object

    def forward(self, mailobj, toemails, **kwargs):
##        return forward(self.email, b85decode(self.pwd).decode(),
##                       mailobj, toemails, **kwargs)
        email = kwargs.get('email') or kwargs.get('fromemail') or mailobj.email
        pwd = kwargs.get('pwd') or mailobj.pwd
        recvers = toemails
        subject = kwargs.get('subject') or mailobj.subject
        body = kwargs.get('body') or mailobj.body
        html = kwargs.get('html') or mailobj.html
        attachments = kwargs.get('attachments') or []
        nofileattach = kwargs.get('nofileattach') or \
                       ({filename: filedata for filename in \
                        mailobj.attachments.file for filedata \
                        in mailobj.attachments.data} if mailobj.attachments else \
                                                   {})
        date = mailobj.date

        prefix = f'''
    ---------- Forwarded message ----------
    From: {email}
    Date: {date}
    Subject: {subject}
    To: {recvers}

    '''
        nsubject = 'Fwd: '+subject
        nbody = prefix + body    
        
        emailobj = copy.deepcopy(mailobj)
        emailobj.msg = list(emailobj.msg)
        emailobj.msg[1] = list(emailobj.msg[1])
        emailobj.msg[1][0] = nsubject
        emailobj.msg[1][1] = nbody
        emailobj.msg[1] = tuple(emailobj.msg[1])
        emailobj.msg = tuple(emailobj.msg)
        
        return self.sendmailobj(emailobj)

    def sendmailobj(self, mailobj, toemails, **kwargs):
##        return sendmailobj(self.email, b85decode(self.pwd).decode(),
##                           mailobj, toemails, **kwargs)
        email = kwargs.get('email') or kwargs.get('fromemail') or mailobj.email
        pwd = kwargs.get('pwd') or mailobj.pwd
        recvers = kwargs.get('recvers') or kwargs.get('toemails') or \
                  mailobj.recvers
        subject = kwargs.get('subject') or mailobj.subject
        body = kwargs.get('body') or mailobj.body
        html = kwargs.get('html') or mailobj.html
        attachments = kwargs.get('attachments') or []
        nofileattach = kwargs.get('nofileattach') or \
                       ({filename: filedata for filename in \
                        mailobj.attachments.file for filedata \
                        in mailobj.attachments.data} if mailobj.attachments \
                        else {})

        return self.send(recvers, subject, body, html, attachments,
                         nofileattach)

    def sendzoominvite(self, invitees, meetingurl, meetingid, meetingpwd):
        invite = genzoominvite(meetingurl, meeting, meetingpwd)
        return self.send(invitees, 'Please join Zoom meeting in progress',
                         invite)

class EmailReader:
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = b85encode(pwd.encode())
        self.conn, self.tls = getserver(email, 'imap')
        if self.tls:
            self.conn.starttls()
        self.conn.login(email, pwd)

    def read(self, foldername = 'INBOX'):
##        return readmail(self.email, b85decode(self.pwd).decode(),
##                        foldername)
        self.conn.select(foldername, readonly = True)
        
        mail = []
        
        subs = []
        bodys = []
        froms = []
        htmls = []
        files = []
        dates = []

        tos = []

        uids = []

        bids = self.conn.search(None, 'ALL')[1][0].split()
        ids = [int(x) for x in bids]

        for x in range(len(ids)):
            msg = self.conn.fetch(bids[x], '(RFC822)')
            msg = _email.message_from_string(msg[1][0][1].decode())
            sub = msg['Subject']
            fr = msg['From']
            to = msg['To'].split(', ')
            date = msg['Date']
            text = None
            html = None
            file = []
            if msg.is_multipart():
                for y in msg.get_payload():
                    if y.get_content_type() == 'text/plain':
                        text = y.get_payload()
                    elif y.get_content_type() == 'text/html':
                        html = y.get_payload()
                    else:
                        file.append({y.get_filename(): y.get_payload()})
            else:
                text = ''.join(msg.get_payload())
                html = '<pre style="font-family:Calibri;">'+text+'</pre>'

            if not text:
                if html:
                    if re.findall(r'<pre(.*)?>(.*)</pre>', html):
                        text = '\n'.join([x[1] for x in \
                                        re.findall(r'<pre(.*)?>(.*)</pre>', html)])

            subs.append(sub)
            bodys.append(str(text))
            froms.append(fr)
            htmls.append(str(html))
            tos.append(to)
            uids.append(ids[x])
            files.append(file)
            dates.append(date)
        

        for x in range(len(ids)):
            t = [self.email]
            
            for y in tos[x]:
                t.append(y)
                
            tos[x] = t

            mail.append((froms[x], (subs[x], bodys[x], htmls[x], files[x],
                                    dates[x]), tos[x][0], uids[x]))

        for x in range(len(mail)):
            mail[x] = EmailMessage(mail[x], self.email,
                                   b85decode(self.pwd).decode())

        if not mail:
            return

        mail = sort(mail)
        mail = EmailMessageList(mail)

        return mail

    def getfoldernames(self):
##        return getfoldernames(self.email, b85decode(self.pwd).decode())
        names = self.conn.list()
        names = names[1]
        allnames = []
        for name in names:
            allnames.append(name.decode().split(' ')[-1].strip('"').rstrip('"'))
        return allnames

    def createfolder(self, foldername):
##        return createfolder(self.email, b85decode(self.pwd).decode(),
##                            foldername)
        return self.conn.create(foldername)

    def deletefolder(self, foldername):
##        return deletefolder(self.email, b85decode(self.pwd).decode(),
##                            foldername)
        return self.conn.delete(foldername)

    def store(uid_s, foldername):
        if type(uid_s) == int or type(uid_s) == bytes:
            uid_s = [uid_s]
        else:
            pass

        for x in range(len(uid_s)):
            if type(uid_s[x]) == int:
                uid_s[x] = str(uid_s[x]).encode()
                
        self.conn.select('INBOX', readonly = False)

        for uid in uid_s:
            self.conn.store(uid, '+X-GM-LABELS', '\\'+foldername)
            
        self.conn.expunge()

class EmailManager:
    def __init__(self, email, pwd):
        self.sender = EmailSender(email, pwd)
        self.reader = EmailReader(email, pwd)
        self.email = email

    def send(self, toemails, subject = '', body = '', html = None,
             attachments = None, nofileattach = None):
        return self.sender.send(toemails, subject, body, html,
                        attachments, nofileattach)

    def read(self, foldername = 'INBOX'):
        return self.reader.read(foldername)

    def sendzoominvite(self, invitees, meetingurl, meetingid, meetingpwd):
##        return sendzoominvite(self.sender.email, b85decode(self.sender.pwd),
##                              invitees, meetingurl, meetingid, meetingpwd)
        return self.sender.sendzoominvite(invitees, meetingurl, meetingid,
                                          meetingpwd)

    def getfoldernames(self):
        return self.reader.getfoldernames()

    def forward(self, mailobj, toemails, **kwargs):
        return self.sender.forward(mailobj, toemails, **kwargs)

    def sendmailobj(self, mailobj, toemails, **kwargs):
        return self.sender.sendmailobj(mailobj, toemails, **kwargs)

    def createfolder(self, foldername):
        return self.reader.createfolder(foldername)

    def deletefolder(self, foldername):
        return self.reader.deletefolder(foldername)

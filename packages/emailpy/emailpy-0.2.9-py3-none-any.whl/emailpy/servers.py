
from .gethostport import gethostport
import smtplib
import imaplib

def getserver(email, mode):
    host, port = gethostport(email, mode)
    if port == 465:
        _class = smtplib.SMTP_SSL
        tls = False
    elif port == 587:
        _class = smtplib.SMTP
        tls = True
    else:
        _class = imaplib.IMAP4_SSL
        tls = False
    return _class(host, port), tls

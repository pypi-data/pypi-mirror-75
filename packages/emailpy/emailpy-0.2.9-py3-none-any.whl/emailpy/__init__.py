__version__ = '0.2.9'
__author__ = 'Sandra Mattar'
__email__ = 'sandrawmattar@gmail.com'
__url__ = 'https://pypi.org/project/emailpy'

"""
A Python interface for interacting with all emails.  
"""

import sys

if not sys.version_info.major == 3:
    class VersionError(BaseException):
        pass
    
    raise VersionError('package "emailpy" requires python 3. ')

from .util import EmailManager
from .gethostport import PROVIDERS, SMTPSERVERS, IMAPSERVERS, SERVERS
from smtplib import SMTP as _Login
_LoginMode = 'smtp'

def login(email, pwd):
    host, port = gethostport(email, _LoginMode)
    try:
        s = _Login(host, port)
        s.ehlo()
        s.starttls()
        s.login(email, pwd)
    except:
        return False
    else:
        return True

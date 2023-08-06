PROVIDERS = (
    '@gmail.com',
    '@outlook.com',
    '@hotmail.com',
    '@yahoo.com',
    '@txt.att.net',
    '@comcast.net',
    '@vtext.com'
    )
SMTPSERVERS = (
    ('smtp.gmail.com', 587),
    ('smtp-mail.outlook.com', 587),
    ('smtp-mail.outlook.com', 587),
    ('smtp.mail.yahoo.com', 587),
    ('smtp.mail.att.net', 465),
    ('smtp.comcast.net', 587),
    ('smtp.verizon.net', 465)
    )
IMAPSERVERS = (
    ('imap.gmail.com', 993),
    ('imap-mail.outlook.com', 993),
    ('imap-mail.outlook.com', 993),
    ('imap.mail.yahoo.com', 993),
    ('imap.mail.att.net', 993),
    ('imap.comcast.net', 993),
    ('incoming.verizon.net', 993)
    )
SERVERS = SMTPSERVERS + IMAPSERVERS

def gethostport(email, mode):
    if mode == 'smtp':
        ssl = 465
        nssl = 587
        if fromemail.endswith('@gmail.com'):
            return 'smtp.gmail.com', nssl
        elif fromemail.endswith('@outlook.com'):
            return 'smtp-mail.outlook.com', nssl
        elif fromemail.endswith('@hotmail.com'):
            return 'smtp-mail.outlook.com', nssl
        elif fromemail.endswith('@yahoo.com'):
            return 'smtp.mail.yahoo.com', nssl
        elif fromemail.endswith('@txt.att.net'):
            return 'smtp.mail.att.net', ssl
        elif fromemail.endswith('@comcast.net'):
            return 'smtp.comcast.net', nssl
        elif fromemail.endswith('@vtext.com'):
            return 'smtp.verizon.net', ssl

    elif mode == 'imap':
        ssl = 993
        if email.endswith('@gmail.com'):
            return 'imap.gmail.com', ssl
        elif email.endswith('@outlook.com'):
            return 'imap-mail.outlook.com', ssl
        elif email.endswith('@hotmail.com'):
            return 'imap-mail.outlook.com', ssl
        elif email.endswith('@yahoo.com'):
            return 'imap.mail.yahoo.com', ssl
        elif email.endswith('@txt.att.net'):
            return 'imap.mail.att.net', ssl
        elif email.endswith('@comcast.net'):
            return 'imap.comcast.net', ssl
        elif email.endswith('@vtext.com'):
            return 'incoming.verizon.net', ssl

    return '', 0

.. _email:

smtpd
=====

smtp server

usage
-----

smtplib
=======

smtp protocol client

usage
-----

import::

    import smtplib

class SMTP::

    smtp = smtplib.SMTP()

    methods:
    smtp.connection(host, port)
    smtp.login(user, password)
    smtp.sendmail(from_addr, to_addrs, msg, mail_options=[], rcpt_options=[])
    smtp.close()
    smtp.quit()

poplib
======

pip3 protocol client

usage
-----

imaplib
=======

imap4 protocol client

usage
-----

email
=====

email and MINE handling package.

usage
-----

import::

    import

class MIMEBase::

    MIMEBase(email.message.Message)

    methods:
    add_header(self, _name, _value, **_params)
    as_string(self, unixfrom=False)
    attach(self, payload)
    del_param(self, param, header='content-type', requote=True)
    is_multipart(self)

class MIMEMultipart::

    # 'Content-Type': 'multipart/*'
    multipart/form-data   post a file in form
    multipart/alternative html or text

    # used for send email with attachment.
    MIMEMultipart(email.mime.base.MIMEBase)

    msg['Subject'] = string
    msg['From'] = string
    msg['To'] = '.'.join(to)
    msg['Cc'] = '.'.join(cc)
    msg['Date'] =  email.utils.formatdate()

class MIMENonMultipart::

    # used for send email without attachment.
    MIMENonMultipart(email.mime.base.MIMEBase)

class MIMEMessage::

    # 'Content-Type': 'message/*'
    message/rfc822

    MIMEMessage(email.mime.nonmultipart.MIMENonMultipart)

class MIMEApplication::

    # 'Content-Type': 'application/*'
    application/xhtml+xml    for xhtml
    application/octet-stream for binary data
    application/pdf          for pdf
    application/msword       for MS word
    application/vnd.wap.xhtml+xml  for wap1.0+
    application/xhtml+xml    for wap2.0+
    application/x-www-form-urlencoded    for http port with form

    MIMEApplication(MIMENonMultipart):

class MIMEText::

    # Content-Type': 'text/*'
    text/plain
    text/html

    MIMEText(email.mime.nonmultipart.MIMENonMultipart)

class MIMEAudio::

    # Content-Type': 'audio/*'
    video/mpeg

    MIMEAudio(email.mime.nonmultipart.MIMENonMultipart)

class MIMEImage::

    # Content-Type': 'image/*'
    image/gif
    image/jpeg
    image/png

    MIMEImage(email.mime.nonmultipart.MIMENonMultipart)





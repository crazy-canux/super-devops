import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate
import logging
import os


logger = logging.getLogger(__name__)
logging.getLogger('smtplib').setLevel(logging.WARNING)
logging.getLogger('email').setLevel(logging.WARNING)


class BaseEmail(object):
    def __init__(
            self, host='localhost', port=25, username=None, password=None
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.smtp = None

    def __enter__(self):
        self.smtp = smtplib.SMTP()
        # self.smtp.set_debuglevel(True)
        self.smtp.connect(self.host, self.port)
        self.smtp.ehlo()
        if self.smtp.has_extn('STARTTLS'):
            self.smtp.starttls()
            self.smtp.ehlo()
        if self.username and self.password:
            self.smtp.login(self.username, self.password)
        logger.debug("BaseEmail.__enter__(): succeed")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.smtp:
            self.smtp.quit()

    def sendmail(
            self, frm, to, subject='', text='',
            files=None, cc=None, date=None
    ):
        try:
            if frm is None:
                raise ValueError("from address is necessary")

            if to is None:
                raise ValueError("to address is necessary")
            elif not isinstance(to, list):
                raise TypeError("to address must be a list")

            if cc:
                if not isinstance(cc, list):
                    raise TypeError("cc should be a list")

            if files:
                if not isinstance(files, list):
                    raise TypeError("files should be a list")

            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = frm
            msg['To'] = '.'.join(to)
            if cc:
                msg['Cc'] = '.'.join(cc)
                to = to + cc
            msg['Date'] = date if date else formatdate()

            text = MIMEText(text)
            msg.attach(text)

            if files:
                for filename in files:
                    with open(filename, 'rb') as f:
                        one = MIMEApplication(f.read())
                    one['Content-Disposition'] = 'attachment; filename={}'.format(
                        os.path.basename(filename))
                    msg.attach(one)
        except Exception as e:
            raise RuntimeError(
                "Perpare to sendmail failed: {}".format(e.message)
            )
        else:
            try:
                self.smtp.sendmail(frm, to, msg.as_string())
            except Exception as e:
                raise RuntimeError("sendmail failed: {}".format(e.message))
            else:
                return True







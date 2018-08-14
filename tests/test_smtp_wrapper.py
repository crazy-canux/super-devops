import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(".."))
from super_devops.email.smtplib_wrapper import BaseEmail


class EmailTestCase(unittest.TestCase):
    def test_sendtext(self):
        with BaseEmail() as email:
            email.sendmail(
                frm="taf@gmail.com",
                to=["canuxcheng@gmail.com"],
                subject='taf test',
                text='i am text'
            )

    def test_sendattach(self):
        with BaseEmail() as email:
            email.sendmail(
                frm="taf@gmail.com",
                to=["canuxcheng@gmail.com"],
                cc=["canuxcheng@gmail.com"],
                subject='taf test',
                text='i am text',
                files=['/home/canux/examples.desktop']
            )


if __name__ == '__main__':
    unittest.main()

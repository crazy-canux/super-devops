import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(".."))
from super_devops.email.smtplib_wrapper import BaseEmail


class EmailTestCase(unittest.TestCase):
    def test_sendtext(self):
        with BaseEmail() as email:
            email.sendmail(
                frm="taf@sonicwall.com",
                to=["wcheng@sonicwall.com"],
                subject='taf test',
                text='i am text'
            )

    def test_sendattach(self):
        with BaseEmail() as email:
            email.sendmail(
                frm="taf@sonicwall.com",
                to=["wcheng@sonicwall.com"],
                cc=["wcheng@sonicwall.com"],
                subject='taf test',
                text='i am text',
                files=['/home/canux/examples.desktop']
            )


if __name__ == '__main__':
    unittest.main()

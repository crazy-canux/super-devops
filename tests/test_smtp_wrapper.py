import unittest

from super_devops.email.smtplib_wrapper import BaseEmail


class EmailTestCase(unittest.TestCase):
    @unittest.skip("ignore")
    def test_sendtext(self):
        with BaseEmail() as email:
            email.sendmail(
                frm="taf@gmail.com",
                to=["canuxcheng@gmail.com"],
                subject='taf test',
                text='i am text'
            )

    @unittest.skip("ignore")
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

    def test_smtpserver(self):
        with BaseEmail(host='mail.company.com', port=25) as email:
            email.sendmail(
                frm="super-devops@company.com",
                to=['canux@company.com'],
                subject='test subject',
                text='text body'
            )


if __name__ == '__main__':
    unittest.main()

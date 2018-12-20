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

    def test_plain(self):
        with BaseEmail(host='mail.domain.com', port=25) as email:
            email.sendmail(
                frm="super-devops@domain.com",
                to=['canuxcheng@gmail.com', 'canuxcheng@163.com'],
                subject='test subject',
                text='text body'
            )

    @unittest.skip('ignore')
    def test_html(self):
        with BaseEmail(host='mail.domain.com', port=25) as email:
            email.sendmail(
                frm="super-devops@domain.com",
                to=['wcheng@domain.com'],
                subject='test subject',
                text='<html><body><h1>text body</h1></body></html>',
                subtype='html', charset='utf-8'
            )


if __name__ == '__main__':
    unittest.main()

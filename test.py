import os
import unittest
from main import validate_input, send_email_mailgun, send_email_sendgrid, get_email_service, get_config, write_config

os.environ['EMAIL_SERVICE_CONFIG'] = os.path.join('test', 'test_config.yaml')

class TestEmailServices(unittest.TestCase):
    def setUp(self):
        self.email = {
            'to': 'crgeorge1021@gmail.com',
            'to_name': 'cg',
            'from': 'chris@em8912.rupainterviewcg.com',
            'from_name': 'chris',
            'subject': 'test1',
            'body': 'test body'
        }
    def test_validate_input(self):
        self.assertTrue(validate_input(self.email))
        self.email.pop('to')
        self.assertFalse(validate_input(self.email))

    def test_mailgun(self):
        response = send_email_mailgun(self.email)
        self.assertTrue(response.status_code == 200)

    def test_sendgrid(self):
        response = send_email_sendgrid(self.email)
        self.assertTrue(response.status == 202)

    def test_flip_email_service_in_config(self):
        original_config = get_config()
        original_config['default_email_service'] = None
        original_config['last_used_email_service'] = 'mailgun'
        write_config(original_config)
        email_service = get_email_service()
        self.assertEqual(email_service, 'sendgrid')
        email_service = get_email_service()
        self.assertEqual(email_service, 'mailgun')

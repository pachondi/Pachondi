from django.test.testcases import TestCase
from app.users.models import SiteUser

class AuthenticationTestCase(TestCase):
    def setUp(self):
        SiteUser.objects.create(self)
        
    def test_unknown_email(self):
        """An unknown email used for login should be restricted"""
        user = SiteUser.objects.get(email='xyztestuser@test.com')        
        self.assertEqual(user, None)
        
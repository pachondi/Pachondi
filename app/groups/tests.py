from django.test import TestCase
from app.groups.models import Group
from app.users.models import SiteUser

class GroupTest(TestCase):
    
    TEST_USER = 'usera@pachondi.com'
    TEST_PASSWORD = 'password'
    
    def setUp(self):
        SiteUser.objects.create(email=self.TEST_USER,password=self.TEST_PASSWORD)
        
        Group.objects.create(owner = SiteUser.objects.get(email=self.TEST_USER),
                             group_name='Group A', group_type=2,
                             summary='A summary', description='A description')

        
    def test_object_created_is_instance_of_group_class(self):
        #create a SiteUser

        groupA =  Group.objects.get(group_name='Group A')
        TestCase.assertIsInstance(self, groupA, Group)    
        

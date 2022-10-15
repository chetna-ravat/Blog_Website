from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            This methods helps creation of initial data at the class level, once for the whole TestCase. 
            This technique allows for faster tests as compared to using setUp().

            Documentation: https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.TestCase.setUpTestData
        """
        cls.client = Client()

        # Create Two user
        cls.user1 = User.objects.create(username='tester1', email="tester1@example.com")
        cls.user1.set_password('tester123')
        cls.user1.save()

        cls.user2 = User.objects.create(username='tester2', email="tester2@example.com")
        cls.user2.set_password('tester234')
        cls.user2.save()


    ### LOGIN / LOGOUT  ###
    def test_user_can_login_succesfully(self):
        login_status = self.client.login(username='tester1', password='tester123')
        
        self.assertTrue(login_status)

    def test_user_can_logout_succesfully(self):
        """
            Test without login we try to create post we get redirected to login page.
        """
        self.client.login(username='tester1', password='tester123')

        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/post/new/")
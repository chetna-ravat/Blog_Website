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


    ### Login/Logout  ###
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
    
    ### Register ###

    def test_register_page_view_accessed_successfully(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
    
    def test_register_page_using_correct_template(self):
        response = self.client.get(reverse("register"))

        self.assertTemplateUsed(response, "users/register.html")
    
    def test_successful_registeration_redirects_to_login_page(self):
        response = self.client.post(reverse('register'), {
            "username": "tester",
            "email": "tester@example.com",
            "password1": "Tester123xyZ",
            "password2": "Tester123xyZ"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")

    def test_registeration_registers_correct_user(self):
        response = self.client.post(reverse('register'), {
            "username": "tester",
            "email": "tester@example.com",
            "password1": "Tester123xyZ",
            "password2": "Tester123xyZ"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(id=3).first().username, "tester")
        self.assertEqual(User.objects.filter(id=3).first().email, "tester@example.com")

    ### Profile
    def test_profile_page_view_access_redirected_to_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/profile/")
        
    def test_profile_page_view_accessed_successfully(self):
        self.client.login(username='tester1', password='tester123')

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

        self.client.logout()
    
    def test_profile_page_using_correct_template(self):
        self.client.login(username='tester1', password='tester123')
        response = self.client.get(reverse("profile"))

        self.assertTemplateUsed(response, "users/profile.html")

        self.client.logout()
    
    def test_profile_update(self):
        self.client.login(username='tester1', password='tester123')

        response = self.client.post(reverse('profile'), {
            "username": "tester1",
            "email": "tester12@example.com",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/profile/")
        self.assertEqual(User.objects.filter(id=1).first().email, "tester12@example.com")

        self.client.logout()
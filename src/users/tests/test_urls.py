from django.urls import reverse, resolve
from django.test import SimpleTestCase
from users.views import register, profile
from django.contrib.auth.views import LoginView, LogoutView

class UserUrlTests(SimpleTestCase):
    """
        Test all urls under users app are getting resolved.
    """
    def test_register_url_is_resolved(self):
        """
            Test register page url is getting resolved properly
        """
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)
    
    def test_profile_url_is_resolved(self):
        """
            Test profile page url is getting resolved properly
        """
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)
    
    def test_login_url_is_resolved(self):
        """
            Test login page url is getting resolved properly
        """
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolved(self):
        """
            Test logout page url is getting resolved properly
        """
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from blog.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, UserPostListView, send_email

class TestUrls(SimpleTestCase):
    """
        Test all urls under blogs are getting resolved.
    """
    def test_home_url_is_resolved(self):
        """
            Test home page url is getting resolved properly
        """
        url = reverse('blog-home')
        self.assertEquals(resolve(url).func.view_class, PostListView)
    
    def test_post_detail_url_is_resolved(self):
        """
            Test post detail page url is getting resolved properly
        """
        url = reverse('post-detail', kwargs = {'pk': 1})
        self.assertEquals(resolve(url).func.view_class, PostDetailView)
        self.assertEquals(resolve(url).kwargs.get('pk'), 1)
    
    def test_post_create_url_is_resolved(self):
        """
            Test post create page url is getting resolved properly
        """
        url = reverse('post-create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)
    

    def test_post_update_url_is_resolved(self):
        """
            Test post update page url is getting resolved properly
        """
        url = reverse('post-update', kwargs = {'pk': 1})
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)
        self.assertEquals(resolve(url).kwargs.get('pk'), 1)

    def test_post_delete_url_is_resolved(self):
        """
            Test post delete page url is getting resolved properly
        """
        url = reverse('post-delete', kwargs = {'pk': 1})
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)
        self.assertEquals(resolve(url).kwargs.get('pk'), 1)
    
    def test_send_email_url_is_resolved(self):
        """
            Test send email page url is getting resolved properly
        """
        url = reverse('send-email', kwargs = {'pk': 1})
        self.assertEquals(resolve(url).func, send_email)
        self.assertEquals(resolve(url).kwargs.get('pk'), 1)
    
    def test_user_post_url_is_resolved(self):
        """
            Test user posts page url is getting resolved properly
        """
        url = reverse('user-posts', kwargs = {'username': 'tester'})
        self.assertEquals(resolve(url).func.view_class, UserPostListView)
        self.assertEquals(resolve(url).kwargs.get('username'), 'tester')
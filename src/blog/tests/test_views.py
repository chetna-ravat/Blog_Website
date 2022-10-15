from this import d
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post
from django.contrib.auth.models import User

class BlogPostTests(TestCase):

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

        cls.post1 = Post.objects.create(
            title="test1 title",
            content="This is test1",
            author=cls.user1
        )
        cls.post2 = Post.objects.create(
            title="test2 title",
            content="This is test2",
            author=cls.user2
        )

    ### Home Page ###
    def test_blog_home_page_view_accessed_successfully(self):
        response = self.client.get(reverse("blog-home"))

        self.assertEqual(response.status_code, 200)
    
    def test_blog_home_page_using_correct_template(self):
        response = self.client.get(reverse("blog-home"))

        self.assertTemplateUsed(response, "blog/home.html")
    
    def test_blog_home_page_loads_correct_posts(self):
        response = self.client.get(reverse("blog-home"))

        self.assertEqual(len(response.context['posts']), 2)
        self.assertEqual(response.context['posts'][0].title, "test2 title")
        self.assertEqual(response.context['posts'][0].content, "This is test2")
        self.assertEqual(response.context['posts'][0].author.username, "tester2")
        self.assertEqual(response.context['posts'][0].author.email, "tester2@example.com")

        self.assertEqual(response.context['posts'][1].title, "test1 title")
        self.assertEqual(response.context['posts'][1].content, "This is test1")
        self.assertEqual(response.context['posts'][1].author.username, "tester1")
        self.assertEqual(response.context['posts'][1].author.email, "tester1@example.com")

    ### Post Detail ###
    def test_post_detail_view_accessed_successfully(self):
        response = self.client.get(reverse('post-detail', kwargs = {'pk': 1}))
        
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_view_using_correct_template(self):
        response = self.client.get(reverse('post-detail', kwargs = {'pk': 1}))

        self.assertTemplateUsed(response, "blog/post_detail.html")
    
    def test_post_detail_view_loads_correct_post(self):
        response = self.client.get(reverse('post-detail', kwargs = {'pk': 1}))

        self.assertEqual(response.context['post'].title, "test1 title")
        self.assertEqual(response.context['post'].content, "This is test1")
        self.assertEqual(response.context['post'].author.username, "tester1")
        self.assertEqual(response.context['post'].author.email, "tester1@example.com")

    ### User Post ###
    def test_user_post_view_accessed_successfully(self):
        response = self.client.get(reverse('user-posts', kwargs = {'username': 'tester1'}))
        
        self.assertEqual(response.status_code, 200)
    
    def test_user_post_view_using_correct_template(self):
        response = self.client.get(reverse('user-posts', kwargs = {'username': 'tester1'}))

        self.assertTemplateUsed(response, "blog/user_posts.html")
    
    def test_user_post_view_loads_correct_post(self):
        response = self.client.get(reverse('user-posts', kwargs = {'username': 'tester1'}))

        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(response.context['posts'][0].title, "test1 title")
        self.assertEqual(response.context['posts'][0].content, "This is test1")
        self.assertEqual(response.context['posts'][0].author.username, "tester1")
        self.assertEqual(response.context['posts'][0].author.email, "tester1@example.com")

    def test_user_post_view_access_fails_with_404(self):
        response = self.client.get(reverse('user-posts', kwargs = {'username': 'tester'}))
        
        self.assertEqual(response.status_code, 404)

    ### Post Create ###
    def test_post_create_view_access_redirected(self):
        response = self.client.get(reverse('post-create'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/post/new/")

    def test_post_create_view_accessed_successfully(self):
        self.client.login(username='tester1', password='tester123')
        response = self.client.get(reverse('post-create'))

        self.assertEqual(response.status_code, 200)
        
        self.client.logout()
        
    def test_post_create_view_using_correct_template(self):
        self.client.login(username='tester1', password='tester123')
        response = self.client.get(reverse('post-create'))

        self.assertTemplateUsed(response, "blog/post_form.html")

        self.client.logout()
    
    def test_post_create_view_creates_correct_post(self):
        self.client.login(username='tester1', password='tester123')

        response = self.client.post(reverse('post-create'), {
            'title': 'Testing new post',
            'content': "It is a brand new post"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.filter(id=3).first().title, "Testing new post")
        self.assertEqual(Post.objects.filter(id=3).first().content, "It is a brand new post")
        self.assertEqual(Post.objects.filter(id=3).first().author.username, "tester1")
        self.assertEqual(Post.objects.filter(id=3).first().author.email, "tester1@example.com")

        self.client.logout()
    
    ### Post Update ###
    def test_post_update_view_access_redirected(self):
        response = self.client.get(reverse('post-update', kwargs = {'pk': 1}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/post/1/update/")

    def test_post_update_view_accessed_successfully(self):
        self.client.login(username='tester1', password='tester123')
        response = self.client.get(reverse('post-update', kwargs = {'pk': 1}))

        self.assertEqual(response.status_code, 200)
        
        self.client.logout()

    def test_post_update_view_using_correct_template(self):
        self.client.login(username='tester1', password='tester123')
        response = self.client.get(reverse('post-update', kwargs = {'pk': 1}))

        self.assertTemplateUsed(response, "blog/post_form.html")

        self.client.logout()

    def test_post_update_view_updated_correct_post(self):
        self.client.login(username='tester1', password='tester123')

        response = self.client.post(reverse('post-update', kwargs = {'pk': 1}), data = {
            'title': 'test1 title Updated',
            'content': "This is test1"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/post/1/")
        self.assertEqual(Post.objects.filter(id=1).first().title, "test1 title Updated")

        self.client.logout()

    ### Post Delete ###
    def test_post_delete_view_access_redirected(self):
        response = self.client.get(reverse('post-delete', kwargs = {'pk': 2}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/post/2/delete/")

    def test_post_delete_view_accessed_successfully(self):
        self.client.login(username='tester2', password='tester234')
        response = self.client.get(reverse('post-delete', kwargs = {'pk': 2}))

        self.assertEqual(response.status_code, 200)
        
        self.client.logout()
    
    def test_post_delete_view_using_correct_template(self):
        self.client.login(username='tester2', password='tester234')
        response = self.client.get(reverse('post-delete', kwargs = {'pk': 2}))

        self.assertTemplateUsed(response, "blog/post_confirm_delete.html")

        self.client.logout()
    
    def test_redirects_to_home_page_after_delete(self):
        self.client.login(username='tester2', password='tester234')

        response = self.client.post(reverse('post-delete', kwargs = {'pk': 2}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        self.client.logout()

    def test_post_delete_view_deletes_correct_post(self):
        self.client.login(username='tester2', password='tester234')

        self.client.post(reverse('post-delete', kwargs = {'pk': 2}))

        response = self.client.get(reverse('post-detail', kwargs = {'pk': 2}))

        self.assertEqual(response.status_code, 404)

        self.client.logout()

    ### (TODO) Send Post via Email ###


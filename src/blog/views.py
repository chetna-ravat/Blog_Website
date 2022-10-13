from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.template import context
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import Http404
from .models import Post
from django.contrib.auth.models  import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from typing import Union
import logging

logger = logging.getLogger(__name__)

def home(request):
    #  lets create a dictionary and call it context, lets create a key named posts and the value of that key will be the data above in the posts list
    context = { 
        'posts': Post.objects.all()
    }
    
    return render (request,'blog/home.html',context) 

def send_email(request, pk):
    user_email = User.objects.filter(username=request.user).first().email
    blog_post = Post.objects.filter(id=pk).first()

    if not user_email:
        logger.warning(f'Failed to send post {pk} via email due to missing user email')
        messages.warning(request, f'Please update correct email in profile')
    else:
        send_mail(
            subject=blog_post.title,
            message=blog_post.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email]
        )
        logger.info(f'Successfully sent post {pk} via email')
        messages.success(request, f'Successfully sent post to {user_email}')
    
    return redirect('post-detail', pk)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'   # <app>/<model>_<viewtype>.html 
    context_object_name = 'posts' 
    # date_posted order the list from oldest to newest, to reverse we add a - sign in the front
    ordering = ['-date_posted']
    paginate_by = 5
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        '''
            return query set consists of posts posted by user and ordered
            by posted date.
        '''
        try: 
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except Http404:
            logger.error("Failed to find username in User model.")
            messages.warning("Something went wrong, can not view posts filtered by user.")
            return
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    fields = ["title", "content"]
    # When we are not defining template_name = <FILENAME>.html in our django defined class function, this means 
    # that django will search for a template with default naming convention of # <app>/<model>_<viewtype>.html 
    # In our PostDetailView function, it is looking for blog/post_detail.html
    # We had passed a template in PostListView since we had already created a template with another name and we
    # wanted django to search for it ,not the file with filename constructed using default naming convention.
    
     
class PostCreateView(LoginRequiredMixin, CreateView):
    # When we are not defining template_name = <FILENAME>.html in our django defined class function, this means 
    # that django will search for a template with default naming convention of # <app>/<model>_form.html 
    # In our PostCreateView & PostUpdateView function, it is looking for blog/post_form.html
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return check_user_and_author_same(self)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        return check_user_and_author_same(self)


### Utility methods ###
def check_user_and_author_same(post_obj: Union[PostDeleteView, PostUpdateView]):
    '''
        Check user in request is same as author of post
    '''
    print(type(post_obj))
    post = post_obj.get_object()
    print(f"{post.author} {post_obj.request.user}")
    if post_obj.request.user == post.author:
        return True
    return False

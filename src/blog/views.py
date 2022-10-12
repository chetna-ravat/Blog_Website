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
from .models import Post
from django.contrib.auth.models  import User
from django.contrib import messages


# Create your views here.


def home (request):
    #  lets create a dictionary and call it context, lets create a key named posts and the value of that key will be the data above in the posts list
    context = { 
        'posts': Post.objects.all()
    }
    return render (request,'blog/home.html',context) 

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
        user = get_object_or_404(User, username=self.kwargs.get('username'))
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
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def sendEmail(request, pk):
    user_email = User.objects.filter(username=request.user).first().email
    if not user_email:
        messages.warning(request, f'Please update correct email in profile')
    else:
        messages.success(request, f'Successfully sent post to {user_email}')
    return redirect('post-detail', pk)



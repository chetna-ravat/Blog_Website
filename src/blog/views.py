from django.shortcuts import render
from django.template import context
from .models import Post

# Create your views here.


def home (request):
    #  lets create a dictionary and call it context, lets create a key named posts and the value of that key will be the data above in the posts list
    context = { 
        'posts': Post.objects.all()
    }
    return render (request,'blog/home.html',context) 
    

def about(request):
    return render (request,'blog/about.html',{'title': 'About' } )



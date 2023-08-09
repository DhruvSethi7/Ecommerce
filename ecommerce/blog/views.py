from django.shortcuts import render
from .models import blogpost as bp
# Create your views here.
from django.http import HttpResponse
def index(request):
    return render(request,"blog/index.html")

def blogpostscreen(request,postid):
    post=bp.objects.filter(post_id=postid)[0]
    print(post)
    {'post': post}
    return render(request,"blog/blogpost.html",{'post':post})

def blogread(request):
    blogs=bp.objects.all()
    print(blogs)
    return render(request,'blog/blogread.html',{'blogs':blogs})

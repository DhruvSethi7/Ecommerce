from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   path("",views.index,name="BlogHome"),
   path("blogread/blogpost/<int:postid>", views.blogpostscreen, name="blogposts"),
   path("blogread/",views.blogread,name="blogread")
]
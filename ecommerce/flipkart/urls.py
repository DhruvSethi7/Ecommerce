from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   path("",views.index,name="FlipkartHome"),
   path("about/",views.about,name="about"),
path("contact/",views.contact,name="contact"),
   path("products/<int:myid>", views.prodView, name="productView"),
]
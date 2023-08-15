from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   path("",views.index,name="FlipkartHome"),
   path("about/",views.about,name="about"),
   path("contact/",views.contact,name="contact"),
   path("products/<int:myid>", views.prodView, name="productView"),
   path("checkout", views.checkout, name="productView"),
   path("tracker", views.tracker, name="tracker"),
   path("verify_payment/", views.verify_payment, name="payverify"),
   path('search/',views.search,name='search')
]
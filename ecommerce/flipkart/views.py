from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import product
def index(request):
    products = product.objects.all()
    return render(request,'flipkart/index.html',{'products': products})

def about(request):
    return render(request,'flipkart/about.html')
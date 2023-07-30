from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import product
from math import ceil
def index(request):
        # products=product.objects.all()
        # print("Id is")
        # print(products[0].id)
        allProds = []
        catprods = product.objects.values('catergory', 'id')
        cats = {item["catergory"] for item in catprods}
        for cat in cats:
            prod = product.objects.filter(catergory=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
        params = {'allProds': allProds}
        return render(request, "flipkart/index.html", params)

def about(request):
    return render(request,'flipkart/about.html')
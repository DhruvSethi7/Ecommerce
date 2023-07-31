from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import product,Contact
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
    print('hii')
    return render(request,'flipkart/about.html')

def contact(request):
    print('hii')
    if(request.method=='POST'):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'flipkart/contact.html')


def prodView(request,myid):
    clickedProduct=product.objects.filter(id=myid);
    print(clickedProduct)
    return render(request,'flipkart/prodView.html',{'product':clickedProduct[0]})
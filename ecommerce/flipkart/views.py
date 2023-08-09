from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
from .models import product,Contact,Orders,OrderUpdate
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
        print('gya ')
        val=True
        return render(request, 'flipkart/contact.html',{'filled':val})
    return render(request,'flipkart/contact.html')


def prodView(request,myid):
    clickedProduct=product.objects.filter(id=myid);
    print(clickedProduct)
    return render(request,'flipkart/prodView.html',{'product':clickedProduct[0]})

def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank=True
        id=order.order_id
        update = OrderUpdate(order_id=id, update_desc="The order has been placed")
        update.save()
        return render(request, 'flipkart/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'flipkart/checkout.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)

                    print(len(updates));
                return HttpResponse(response)
            else:
                return HttpResponse('{snn}')
        except Exception as e:
            return HttpResponse('{www}')

    return render(request, 'flipkart/tracker.html')
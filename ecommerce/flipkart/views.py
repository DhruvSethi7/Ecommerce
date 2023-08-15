from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
from .models import product,Contact,Orders,OrderUpdate
from math import ceil
import razorpay
from django.conf import settings
client = razorpay.Client(auth=("", ""))
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

def search(request):
    query=request.GET.get('search')
    print(query)
    allProds = []
    catprods = product.objects.values('catergory', 'id')
    cats = {item["catergory"] for item in catprods}
    for cat in cats:
        prod=[]
        tempprod = product.objects.filter(catergory=cat)
        for p in tempprod:
            if query in p.product_name.lower() :
                prod.append(p)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        msg=''
        if len(prod)!=0:
            msg='2'
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds,'msg':msg}
    return render(request,'flipkart/search.html',params)

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
        amount=request.POST.get('amount','')
        print(amount)
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        razorpay_amount = int(float(amount) * 100)
        DATA = {
            "amount":razorpay_amount,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        razorpay_order = client.order.create(data=DATA)
        order = Orders(status='started',items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone, amount=amount,order_id=razorpay_order['id'])
        order.save()
        context = {
            'order_id': razorpay_order['id'],
            'key': "rzp_test_NU5rDHWG0xge0G",
            'amount': razorpay_amount,
            'currency': 'INR',
            'name': 'BharatBazaar',
            'description': 'Test Transaction',
            'image': 'https://example.com/your_logo.jpg'
        }
        return render(request, "flipkart/payment.html",context )
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




def verify_payment(request):
    print('mein agya hu')
    if request.method == "GET":
        # Get payment details from the request
        razorpay_payment_id = request.GET.get('payment_id')
        razorpay_order_id = request.GET.get('order_id')

        # Fetch the payment from Razorpay
        try:
            payment = client.payment.fetch(razorpay_payment_id)
            print(f"payment is ${payment}");

            # Check if the payment's `order_id` matches and the payment status is "captured"
            if payment['order_id'] == razorpay_order_id and payment['status'] == 'captured':
                # Mark the order as paid in your database
                order = Orders.objects.get(order_id=razorpay_order_id)
                order.status = 'Paid'
                order.save()

                # Optionally, send an email or notification to the user about successful payment

                # Redirect to a success page
                return render(request, 'flipkart/success.html')
            else:
                # Handle the failure - maybe the payment was authorized but not captured.
                # Depending on the business logic, you might want to capture the payment here or refund it.
                return render(request, 'flipkart/failed.html',
                              {'reason': 'Payment was not successfully captured.'})

        except Exception as e:
            # Handle exceptions - maybe log them for monitoring purposes
            return HttpResponse(str(e))

    return HttpResponse("Invalid request method.")

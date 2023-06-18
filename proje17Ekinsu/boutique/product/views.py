from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
import iyzipay
import json
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
import pprint
# index sayfamı görüntülemek için:
def index(request):
    products = Product.objects.all()
    kategoriler = Kategori.objects.all()
    search = '' 
    if request.GET.get('search'):
        search = request.GET.get('search')
        products = Product.objects.filter(
            Q(isim__icontains = search) |
            Q(kategori__isim__icontains = search)
        )
    if request.method == 'POST':
        if request.user.is_authenticated:
            productId = request.POST['productId']
            productm = Product.objects.get(id = productId)
            number = request.POST['number']
            if Basket.objects.filter(owner = request.user, product = productm, payment = False).exists():
                basket = Basket.objects.get(owner = request.user, product = productm, payment = False)
                basket.number += int(number)
                basket.totalPrice = basket.number * basket.product.fiyat
                basket.save()
                messages.success(request, 'Added to basket')
                return redirect('index')
            else:
                basket = Basket.objects.create(
                    owner = request.user,
                    product = productm,
                    number = number,
                    totalPrice = int(number) * productm.fiyat
                )
                basket.save()
                messages.success(request, 'Added to basket')
                return redirect('index')
        else:
            messages.warning(request, 'Please login.')
            return redirect('index')
    context ={
        'products':products,
        'search':search,
        'kategoriler':kategoriler
    }
    return render(request, 'index.html', context)

api_key = 'sandbox-ZIm4AZ9VTiff4gffaV004uUhfKva3ccJ'
secret_key = 'sandbox-VpwaN567pQntiDfeRvUjHLodMznlCiAu'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()


def payment(request):
    context = dict()
    payment = Payment.objects.get(owner = request.user, payment = False)
    buyer={
        'id': str(payment.owner.id),
        'name': payment.owner.username,
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': payment.totalPrice,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Successful TRANSACTIONS'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Unsuccessful'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)



def success(request):
    context = dict()
    context['success'] = 'Transaction Successful'

    messages.success(request, 'Payment successful')
    return redirect('index')


def fail(request):
    context = dict()
    context['fail'] = 'Operation Failed'

    template = 'fail.html'
    return render(request, template, context)




def basket(request):
    user = request.user
    baskets = Basket.objects.filter(owner = user, payment = False)
    total = 0
    for i in baskets:
        total += i.totalPrice
    if request.method == 'POST':
        if 'delete' in request.POST:
            productId = request.POST['productId']
            deleted = Basket.objects.get(id = productId)
            deleted.delete()
            messages.success(request, 'The product has been removed from the basket.')
            return redirect('basket')
        if 'payment' in request.POST:
            if Payment.objects.filter(owner = request.user, payment = False).exists():
                return redirect('payment')
            else:
                payment = Payment.objects.create(
                    owner = request.user,
                    totalPrice = total
                )
                payment.basket.add(*baskets)
                payment.save()
                return redirect('payment')
    context = {
        'baskets': baskets,
        'total':total
    }
    return render(request, 'basket.html', context)
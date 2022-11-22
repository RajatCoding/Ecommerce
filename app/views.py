from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . models import Product, Cart, Product_Status
from .forms import *
import random
from .forms import UserRegisterForm, ProfileUpdateForm, AddOtherAddressForm
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests
from api.serializers import UserSerializer,ProfileUpdateSeializer

User = get_user_model()

votp = None
# Home


def home(request):
    jeans = Product.objects.filter(category="jeans")
    mobile = Product.objects.filter(category="mobile")
    return render(request, 'app/home.html', {"jeans": jeans, "mobile":mobile})


def mobile(request):
    mobile = Product.objects.filter(category="mobile")
    return render(request, "app/mobile.html", {"mobile":mobile})

def laptop(request):
    laptops = Product.objects.filter(category="laptop")
    return render(request, "app/laptop.html", {"laptops":laptops})

def topwear(request):
    topwears = Product.objects.filter(category="t-shirts")
    return render(request, "app/topwear.html", {"topwears":topwears})

def bottomwear(request):
    bottomwears = Product.objects.filter(category="jeans")
    return render(request, "app/bottomwear.html", {"bottomwears":bottomwears})


#-----------------------------------------------------------------------------


# Registration of User & Profile Update

def send_otp(phone_no):
    # Otp send to user who want to register
    # need to add throttling
    # url = "https://www.fast2sms.com/dev/bulkV2"
    otp = random.randint(1000, 9999)
#     querystring = {"authorization":"w5FEkpLNnWScI9CmJ3ZsVXDHberaOgqYtUix76u8KAMzo2QBfd6bNrnQg3ViSLFIeuka5yZYf8TH4CxA","variables_values":otp,"route":"q","numbers":phone_no}

#     headers = {
#     'cache-control': "no-cache"
# }

#     response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    api_key = '82bd6b1b-125c-11ed-9c12-0200cd936042'
    otp = random.randint(1000, 9999)
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_no}/{otp}"
    response = requests.get(url)
    return otp

def customerregistration(request):
    # Registration form
    if request.user.is_anonymous:
        if request.method == "POST":
            global forma
            forma = UserRegisterForm(request.POST)
            if forma.is_valid():
                phone_number = forma.cleaned_data['mobile_no']
                global otp
                otp = send_otp(phone_number)
                print(otp)
                messages.success(request, 'Otp has been sent to your mobile n.o')
                global votp
                votp = random.randint(1000,10000)
                return redirect("/verify_otp/"+str(votp))
        else:
            forma = UserRegisterForm()

        return render(request, 'app/customerregistration.html', {"forms": forma})
    else:
        return redirect("/")

def verify_otp(request,pk):
    # verify otp and save user to database
    if votp is not None:
        if int(pk) == int(votp):
            if request.method == 'POST':
                form = VerifyOtpForm(request.POST)
                if form.is_valid():
                    otp_value = form.cleaned_data['Otp']
                    if int(otp_value) == otp:

                        forma.save()
                        messages.success(request, 'You are registered successfully')
                        return redirect("/login/")
                    else:
                        messages.warning(request, "Sorry invalid Otp please try again")
                        return redirect(customerregistration)

            else:
                form = VerifyOtpForm()
                return render(request, 'app/verify_otp.html', {'form': form})
        else:
            return redirect(customerregistration)
    else:
            return redirect(customerregistration)

@method_decorator(login_required(login_url='login'), name="dispatch")
class ProfileUpdate(UpdateView):
    # User can edit his current profile
    model = User
    form_class = ProfileUpdateForm
    template_name = 'app/profile.html'
    success_url = '/'
    extra_context = {"active": "btn-primary"}

    def dispatch(self, request, *args, **kwargs):
        obj =  self.get_object()
        if obj != self.request.user:
            return redirect("/")
        else:
            return super().dispatch(request, *args, *kwargs)

# ------------------------------------------------------------------------------

# Addresses of User.

def add_address(request, pk):
    # Add address
    if not request.user.is_anonymous :
        if request.user.id == pk:
            if request.method == "POST":
                form = AddOtherAddressForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user_id = pk
                    obj.save()
                    return redirect('profile', pk=pk)
            else:
                form = AddOtherAddressForm()
            return render(request, 'app/address.html', {'form': form})
        else:
            return redirect('/')
    else:
        messages.warning(request, "Don't try to login in others account")
        return redirect('/login')

def manage_address(request, pk):
    # Show and option for delete or edit created address
    if not request.user.is_anonymous :
        if request.user.id == pk:
            add = Customer.objects.filter(Q(user_id=pk) & Q(user_address = False))
            print(add)
            main_add = Customer.objects.filter(Q(user_id=pk) & Q(user_address = True))
        
            return render(request, "app/addressmanage.html", {'active': 'btn-primary', "add": add, "main_add":main_add})
        else:
            return redirect('/')
    else:
            messages.warning(request, "Don't try to login in others account")
            return redirect('/login')

@method_decorator(login_required(login_url='login'), name='dispatch')
class AddressUpdate(UpdateView):
    # Edit address
    model = Customer
    form_class = AddressUpdateForm
    template_name = 'app/addressupdate.html'
    success_url = '/'
    cid = Customer.id
    extra_context = {"active": "btn-primary", "cid": cid}

    def dispatch(self, request, *args, **kwargs):
        obj =  self.get_object()
        if obj.user != self.request.user:
            return redirect("/")
        else:
            return super().dispatch(request, *args, *kwargs)

@method_decorator(login_required(login_url='login'), name='dispatch')
class AddressDelete(DeleteView):
    # Delte Address
    model = Customer
    context_object_name = 'object'
    template_name = 'app/addressdelete.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        obj =  self.get_object()
        if obj.user != self.request.user:
            return redirect("/")
        else:
            return super().dispatch(request, *args, *kwargs)

# ------------------------------------------------------------------------------

# Product

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        item_in_cart = False
        item_in_cart = Cart.objects.filter(
            Q(user=request.user) & Q(product=product.id)).exists()
        return render(request, 'app/productdetail.html', {"product": product, 'items': item_in_cart})
    else:
        return render(request, 'app/productdetail.html', {"product": product})

def add_to_cart(request, pk):
    if not request.user.is_anonymous :
            product = Product.objects.get(id=pk)
            user = request.user
            item = Cart.objects.filter(
                Q(user=request.user) & Q(product=product.id)).exists()
            if item:
                return redirect('/showcart')
            else:
                item = Cart(user=user, product=product).save()
                return redirect('/showcart')
    else:
            messages.warning(request, "Don't try to login in others account")
            return redirect('/login')

@login_required(login_url='login')
def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        amount = 0
        shipping_charges = 70
        if cart_product:
            for p in cart_product:
                amount += p.quantity*p.product.discounted_price

            total_amount = amount+shipping_charges
            return render(request, 'app/addtocart.html', {"carts": carts, "amount": amount, "total_amount": total_amount})
        else:
            return render(request, "app/emptycart.html")
    else:
        return render(request, "app/emptycart.html")


# Cart Quantity


def plus(request):
    if not request.user.is_anonymous :
            if request.method == "GET":
                try:
                   
                    prod_id = request.GET['prod_id']
                    print(prod_id)
                    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
                    c.quantity += 1
                    c.save()
                    cart_product = [p for p in Cart.objects.all() if p.user ==
                                    request.user]
                except:
                    return redirect("/")
                amount = 0
                shipping_amount = 70
                for p in cart_product:
                    amount += p.quantity*p.product.discounted_price
            
                data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
                         }
                return JsonResponse(data)
            

    else:
        messages.warning(request, "Don't try to login in others account")
        return redirect('/login')

def minus(request):
    if not request.user.is_anonymous :
        if request.method == 'GET':
            try:
                prod_id = request.GET['prod_id']
                c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
                c.quantity -= 1
                c.save()
                cart_product = [p for p in Cart.objects.all() if p.user ==
                                request.user]
            except:
                return redirect("/")
        amount = 0
        shipping_amount = 70
        for p in cart_product:
            amount += p.quantity*p.product.discounted_price

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        messages.warning(request, "Don't try to login in others account")
        return redirect('/login')

def remove_cart(request):
    if not request.user.is_anonymous :
        if request.method == 'GET':
            try:
                prod_id = request.GET['prod_id']
                c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
                c.delete()
                amount = 0.0
                shipping_amount = 70.0
                cart_product = [p for p in Cart.objects.all() if p.user ==
                                request.user]
            except:
                return redirect("/")
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

            data = {
                'amount': amount,
                'totalamount': amount+shipping_amount
            }

            return JsonResponse(data)
        else:
            return HttpResponse("")
    else:
        messages.warning(request, "Don't try to login in others account")
        return redirect('/login')


# Placed Order


@login_required(login_url='login')
def checkout(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    amount = 0
    shipping_charges = 70
    if cart_product:
        for p in cart_product:
            amount += p.quantity*p.product.discounted_price
        total_amount = amount+shipping_charges
    address = Customer.objects.filter(Q(user = user) & Q(user_address = False))
    main_add = Customer.objects.filter(Q(user = user) & Q(user_address = True))
    return render(request, 'app/checkout.html', {"carts": carts, "totalamount": total_amount, "address": address, "main_add":main_add})

def paymentdone(request):
    if not request.user.is_anonymous :
        try:
            custid = request.GET.get("custid")
            custom = Customer.objects.get(id=custid)
            print(custom)
            user = request.user
            cart = Cart.objects.filter(user=user)
        except:
             return redirect('/')
        for p in cart:
            Product_Status(user=user, product=p.product,
                        quantity=p.quantity, customer=custom).save()
            p.delete()
        return redirect('/orders')
        

    else:
        messages.warning(request, "Don't try to login in others account")
        return redirect('/login')
        
@login_required(login_url='login')
def buy_now(request, pk):
    user = request.user
    item = Product.objects.get(pk=pk)
    total_amount = 70+ item.discounted_price
    address = Customer.objects.filter(Q(user = user) & Q(user_address = False))
    main_add = Customer.objects.filter(Q(user = user) & Q(user_address = True))
    return render(request, 'app/checkout.html', {"item": item, "total_amount": total_amount, "address": address, "main_add":main_add})

@login_required(login_url='login')
def orders(request):
    user = request.user
    order_placed = Product_Status.objects.filter(user=user)
    return render(request, 'app/orders.html', {"order_placed": order_placed})

import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = UserSerializer


@api_view(['GET',"PUT"])
def profile_edit(request,pk):
    if request.method == "GET":
        profile = User.objects.get(id=pk)
        print(pk)
        print(profile)

        serialize = ProfileUpdateSeializer( profile)
        return Response({"data": serialize.data})
       
        
    if request.method == "PUT":
        profile = User.objects.get(id=pk)
        print(pk)
        print(profile)

        serialize = ProfileUpdateSeializer(profile, data = request.data, partial=True)
        if serialize.is_valid():
            serialize.save()
            return Response({"data": serialize.data})
        else:
            return Response({'msg':"data not updated"})
        



            

            
       
        


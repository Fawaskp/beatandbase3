from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from user_profile.models import User_Address
from user_home.models import CustomUser
from admin_products.models import Product
from admin_variant.models import Product_Variant,Coupon
from django.http import JsonResponse
from user_profile.forms import AddressForm
from user_profile.models import User_Address
import razorpay
from django.conf import settings
from cart.models import Cart,CartItem
from orders.models import Payment_methods
from django.http import HttpResponseRedirect
from django.contrib import messages


def verify_variants(request):
    if request.POST.get('action') == 'post':

        try:
            cart = user = request.user, status = True
        except:
            return JsonResponse({'status':False, 'message':'something went wrong'})
        
        cart_items = CartItem.objects.filter(cart=cart)

        if CartItem.objects.filter(cart = cart, variant__quantity__lt = 0).exists():
            return JsonResponse({'status':False, 'message':'Some products are Out of stock'})

        return JsonResponse({'status':True})
    else:
        return JsonResponse('sorry something went wrong',safe=False)


@login_required(login_url='user_login')
def checkout(request):

    global context
    if request.POST.get('action') == 'post':
        variant_id = request.POST.get('product_variant')
        variant = Product_Variant.objects.get(id = variant_id)
        product_id = request.POST.get('product_id')
        pro_qty = request.POST.get('product_quantity')
        user = CustomUser.objects.get(id=request.user.id)
        shipping_address = User_Address.objects.filter(user = user).order_by('id')
        global gst
        sub_total = (int(variant.price) * int(pro_qty)) 
        gst = sub_total * 0.05
        global total
        total = sub_total + gst + 100 
        form = AddressForm()
        global context
        context = {
            'shipping_address':shipping_address,
            'variant':variant,
            'quantity':pro_qty,
            'gst':gst,
            'total':total,
            'form':form,
            'payment_methods': Payment_methods.objects.all()
            }

        return JsonResponse({'result':'successful'})
    else:

        client  = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        
        if total <= 500000:
            payment = client.order.create({'amount':total*100,'currency':'INR', 'payment_capture': 1})
        else:
            payment = client.order.create({'amount':1*100,'currency':'INR', 'payment_capture': 1})
        
       
        context.update(shipping_address = User_Address.objects.filter(user = request.user.id).order_by('id'))
        context.update(payment = payment)
        return render(request,'checkout/checkout.html',context)


def cart_checkout(request):

    cartdb = Cart.objects.get(user = request.user, status = True)
    items = CartItem.objects.filter(cart = cartdb, variant__quantity__gt = 0)

    if not items:
        messages.error(request,'You are trying to order out of stock product')
        referer = request.META['HTTP_REFERER']
        return HttpResponseRedirect(referer)

    global sub_total
    sub_total = 0
    for item in items:
        sub_total += item.variant.price * item.qty

    after_discount = 0
    if cartdb.coupon:
        after_discount = sub_total - cartdb.coupon_discount

    global gst
    gst = sub_total *0.05
    global grand_total
    if not after_discount == 0:
        grand_total = after_discount + gst + 100
    else:
        grand_total = sub_total + gst + 100


    shipping_address = User_Address.objects.filter(user = request.user)
    form = AddressForm()

    # print('sub_total:',sub_total,' total:',grand_total,' gst:',gst)

    cart,_ = Cart.objects.get_or_create(user = request.user, status = True)
    cart_items = CartItem.objects.filter(cart = cart)
    
    context  = {
        'variants':items,
        'shipping_address':shipping_address,
        'sub_total':sub_total,
        'gst':gst,
        'form':form,
        'total':grand_total,
        'coupon_cart':cartdb,
        'payment_methods': Payment_methods.objects.all(),
        'coupon_cart':cart,
        'cart':cart_items,
        'coupons':Coupon.objects.all(),
    }

    client  = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    if grand_total <= 500000:
        payment = client.order.create({'amount':grand_total*100,'currency':'INR', 'payment_capture': 1})
    else:
        payment = client.order.create({'amount':1*100,'currency':'INR', 'payment_capture': 1})
    

    
    context.update(shipping_address = User_Address.objects.filter(user = request.user.id).order_by('id'))
    context.update(payment = payment)
    
    return render(request,'checkout/cart_checkout.html',context)




def add_address_checkout(request):
    address = User_Address.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            referer = request.META['HTTP_REFERER']
            return HttpResponseRedirect(referer)
        else:
            messages.error(request,'give valid inputs')
            referer = request.META['HTTP_REFERER']
            return HttpResponseRedirect(referer)
    else:
        form = AddressForm()


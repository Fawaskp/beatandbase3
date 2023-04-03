from django.shortcuts import render,redirect
from user_home.models import CustomUser
from user_profile.models import User_Address
from admin_variant.models import Product_Variant,Coupon
from django.http import JsonResponse
from .models import Order,Order_item,Payment_methods
from decimal import Decimal
from cart.models import Cart,CartItem
from cart.cart import Cart as Cart_session
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator

def place_order(request):
    
    if request.POST.get('action') == 'post' and request.POST.get('from') == 'cart':

        # getting user details
        user = request.user
        user = CustomUser.objects.get(id = user.id)

        # getting cart details    
        cartdb = Cart.objects.get(user=user, status=True)
        cart_items = CartItem.objects.filter(cart=cartdb)
        
        # getting values form requests
        total = float(request.POST.get('total') )
        gst = float(request.POST.get('gst') )
        address_id = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        payment_id = request.POST.get('payment_id')


        # getting needed instances from id's
        shipping_address = User_Address.objects.get(id = address_id)
        payment_method = Payment_methods.objects.get(id = payment_method)

        # ensuring wallet balance if order from wallet
        if payment_method.method == 'Wallet':
            usr  = CustomUser.objects.filter(email=request.user)
            wallet_balance = usr[0].wallet
            if wallet_balance < 1:
                return JsonResponse({"message":"You don't have wallet balance","status":False})
            elif wallet_balance < total:
                return JsonResponse({"message":"Insufficient balance in your wallet","status":False})
            else:
                pass

        variant_instance = Product_Variant.objects.all()

        # placing order & reducing the existing stock
        current_order = Order.objects.create(customer=user, address=shipping_address,gst=gst, total=total, payment_method=payment_method, payment_id=payment_id)
        if cartdb.coupon:
            current_order.coupon = cartdb.coupon.name
            current_order.coupon_discount = cartdb.coupon_discount
            current_order.save()

            coupon_obj = Coupon.objects.get(name = cartdb.coupon.name)
            coupon_obj.quantity -= 1
            coupon_obj.save()

        for variant in cart_items:
            variant_instance = Product_Variant.objects.get(id = variant.variant.id)
            variant_instance.quantity -= int(variant.qty)
            variant_instance.save() 
            Order_item.objects.create(order=current_order,variant=variant.variant,quantity=variant.qty)

         # reducing the money from wallet after order
        if payment_method.method == 'Wallet':
            wallet_balance = usr[0].wallet
            wallet_balance -= Decimal(str(total))
            usr.update(wallet=wallet_balance)

        
        session_instance  = Cart_session(request)
        Cart_session.delete_cart(session_instance)

        # making order placed status FALSE
        cartdb.status = False
        cartdb.delete()

        return JsonResponse({'order_id':current_order.id,'address_id':shipping_address.id})
        
    elif request.POST.get('action') == 'post' and request.POST.get('from') == 'direct':

        # getting user details
        user = request.user
        user = CustomUser.objects.get(id = user.id)

        # getting order variant values form requests
        total = float(request.POST.get('total') )
        variant = int(request.POST.get('variant') )
        quantity = int(request.POST.get('quantity') )
        gst = float(request.POST.get('gst') )
        address_id = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        # getting needed instances from id's
        shipping_address = User_Address.objects.get(id = address_id)
        payment_method = Payment_methods.objects.get(id = payment_method)
        variant = Product_Variant.objects.get(id = variant)


        # ensuring wallet balance if order from wallet
        if payment_method.method == 'Wallet':
            usr  = CustomUser.objects.filter(email=request.user)
            wallet_balance = usr[0].wallet
            if wallet_balance < 1:
                return JsonResponse({"message":"You don't have wallet balance","status":False})
            elif wallet_balance < total:
                return JsonResponse({"message":"Insufficient balance in your wallet","status":False})
            else:
                pass

        # placing order and checking whethere it have any exceptions
        try:
            current_order = Order.objects.create(customer=user, address=shipping_address,gst=gst, total=total, payment_method=payment_method)
        except:
            return JsonResponse({"message":"something went wrong, can't place order at this moment","status":'False'})
        Order_item.objects.create(order=current_order,variant=variant,quantity=quantity,user=request.user)

        # reducing the quantity of the ordered stock 
        variant.quantity -= quantity
        variant.save()

        # reducing the money from wallet after order
        if payment_method.method == 'Wallet':
            wallet_balance = usr[0].wallet
            wallet_balance -= Decimal(str(total))
            usr.update(wallet=wallet_balance)

        return JsonResponse({'order_id':current_order.id,'address_id':shipping_address.id})
        



def order_invoice(request):
    # getting order item details for showing in invoice
   try:
    order_id = int(request.GET.get('id'))
    address_id = int(request.GET.get('addrs'))
   except:
        return JsonResponse('Got unexpected values',safe=False)

   order = Order.objects.get(id = order_id)
   order_item = Order_item.objects.filter(order=order)
   
   try:
       shipping_address = User_Address.objects.get(id = address_id,user = request.user)
   except:
       return JsonResponse('Wrong value ?!',safe=False)

    # calculating toal amout of order 
   def get_sub_total():
       sub_total = 0
       for item in order_item:
           sub_total += int(item.variant.price) * int(item.quantity)

       return sub_total
   
   context = {
      'shipping_address':shipping_address,
      'order':order,
      'items':order_item,
      'sub_total':get_sub_total()
   }

   return render(request,'orders/invoice2.html',context)



@login_required(login_url='user_login')
def user_orders(request):

    Ordsdfsdfsdfasers = Order.objects.filter(customer=request.user).order_by('-id')
    order_items = Order_item.objects.filter(order__customer=request.user)

    paginator = Paginator(Ordsdfsdfsdfasers,3)
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)

    context = {
        'orders': page_orders,
        'order_items': order_items,
    }
    return render(request,'orders/user_orders.html',context)


@login_required
def cancel_order(request):

        order_id = request.POST.get('order')
        item_id = request.POST.get('item')

        order = Order.objects.get(id=order_id)
        item = Order_item.objects.get(order=order, id=item_id)
        method = order.payment_method
        
        item_amount = item.get_total()
        if  method.method == 'Razorpay':
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_id = order.payment_id
            refund = client.payment.refund(payment_id,{'amount':item_amount})
        elif method.method == 'Wallet':
            usr  = CustomUser.objects.filter(email=request.user)
            wallet_balance = usr[0].wallet
            wallet_balance += Decimal(str(item_amount))
            usr.update(wallet=wallet_balance)


        item.status = 'cancelled'
        quantity = item.quantity
        item.quantity += quantity
        item.save()

        current_user = request.user
        subject = "Cancell order succesfull!"
        mess = f'Greetings {current_user.first_name}.\nYour Order {order.order_id} has been cancelled. \nThank you for shopping with us!'
        send_mail(
                subject,
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.email],
                fail_silently = False
                )
       
        return JsonResponse({'massage':'success','status' :True})

@login_required
def refund_order(request):
        order_id = request.POST.get('order')
        item_id = request.POST.get('item')

        order = Order.objects.get(id=order_id)
        item = Order_item.objects.get(order=order, id=item_id)
        method = order.payment_method
        
        item_amount = item.get_total()

        if  method.method == 'Razorpay':
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_id = order.payment_id
            refund = client.payment.refund(payment_id,{'amount':item_amount})
        else:
            usr  = CustomUser.objects.filter(email=request.user)
            wallet_balance = usr[0].wallet
            wallet_balance += Decimal(str(item_amount))
            usr.update(wallet=wallet_balance)


        item.status = 'refunded'
        quantity = item.quantity
        item.quantity += quantity
        item.save()

        current_user = request.user
        subject = "Refund succesfull!"
        mess = f'Greetings {current_user.first_name}.\nYour refund for the product {item} of order: {order.order_id} has been succesfully generated. \nThank you for shopping with us!'
        send_mail(
                subject,
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.email],
                fail_silently = False
                )
       
        return JsonResponse({'massage':'success','status' :True})




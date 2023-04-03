from django.shortcuts import render,redirect
from admin_products.models import Product
from django.shortcuts import get_object_or_404
from .cart import Cart as Cart_session
from admin_variant.models import Product_Variant, Coupon
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItem
from user_home.models import CustomUser



def cart_summary(request):

    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user = request.user, status = True)
        cart_items = CartItem.objects.filter(cart = cart)

        def get_total():
            cart_items = CartItem.objects.filter(cart = cart, variant__quantity__gt = 0)
            global sub_total
            sub_total = 0
            for item in cart_items:
                sub_total +=item.variant.price * item.qty

            after_discount = 0
            if cart.coupon:
                after_discount = sub_total - cart.coupon_discount

            global gst
            gst = sub_total *0.05
            global grand_total
            if not after_discount == 0:
                grand_total = after_discount + gst + 100
            else:
                grand_total = sub_total + gst + 100
            return sub_total

        variants = Product_Variant.objects.all()
        return render(request,'cart/cart.html',{'coupon_cart':cart,'cart':cart_items,'variants':variants,'sub_total':get_total(),'gst':gst,'grand_total':grand_total })

    else:
        cart = Cart_session(request)
        return render(request,'cart/cart2.html')
        


def cart_add(request):

    if request.POST.get('action') == 'post':

        if request.user.is_authenticated:

            # getting user 
            user = request.user
            user = CustomUser.objects.get(id = user.id)

            # getting cart item 
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity'))
            variant = request.POST.get('product_variant')


            # # getting needed cart item details from models
            # product = get_object_or_404(Product, id=product_id)
            variant_instance = Product_Variant.objects.get(id = variant)
            # price = variant_instance.price
            # color = variant_instance.color


            # saving cart to database
            cartdb, _ = Cart.objects.get_or_create(user = user, status = True)
            try: 
                CartItem.objects.get(cart=cartdb, variant=variant_instance)
            except:
                item = CartItem.objects.create( cart = cartdb, variant=variant_instance, qty=product_quantity )
                item.save()
            else:
                response = JsonResponse({'message':'sorry something went wrong'})


            # getting count of total cart items 
            cart_item = CartItem.objects.filter(cart = cartdb)
            cart_quantity = 0
            for itm in cart_item:
                cart_quantity+=1

            response = JsonResponse({'qty': product_quantity,'cart_qty':cart_quantity})
            return response
        
        else:
            cart = Cart_session(request)
            product_quantity = int(request.POST.get('product_quantity'))
            variant = request.POST.get('product_variant')
            variant_instance = Product_Variant.objects.get(id = variant)

            # save to session
            cart = Cart_session(request)
            cart.add(variant=variant_instance, variant_qty=product_quantity)

            response = JsonResponse({'status':'sucess'})
            return response
    
def add_quantity(request):

    if request.POST.get('action') == 'post':

        product_id = request.POST.get('product_id')

        response = JsonResponse({'result':f'its working,{product_id}'})
        return response


def cart_delete(request):

    cart = Cart_session(request)

    if request.POST.get('action') == 'post':

        if request.user.is_authenticated:
            variant_id = int(request.POST.get('variant_id'))
            variant_instance = Product_Variant.objects.get(id = variant_id)

            cart.delete(variant=variant_id)

            # delete cart from db
            cartdb = Cart.objects.get(user = request.user, status = True)
            item = CartItem.objects.get(cart = cartdb, variant=variant_instance )
            item.delete()

            cart_item = CartItem.objects.filter(cart = cartdb)
            cart_quantity = 0
            for itm in cart_item:
                cart_quantity+=1


            cart_total = cartdb.total_item_price()
            if cartdb.coupon:
                cart_total -= cartdb.coupon_discount

            
            response = JsonResponse({'qty':cart_quantity, 'total':cart_total})
            return response
        
        else:
            variant_id = int(request.POST.get('variant_id'))

            cart.delete(variant=variant_id)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()

            response = JsonResponse({'qty':cart_quantity, 'total':cart_total})
            return response




def cart_update(request):

    # cart = Cart_session(request)
    if request.POST.get('action') == 'post':

        if request.user.is_authenticated:

            variant_id = int(request.POST.get('variant_id'))
            product_quantity = int(request.POST.get('product_quantity'))

            # cart.update(variant=variant_id, qty=product_quantity)
        

            variant_instance = Product_Variant.objects.get(id = variant_id)
            cartdb = Cart.objects.get(user = request.user, status = True)
            item = CartItem.objects.get(cart = cartdb, variant=variant_instance )
            item.qty = product_quantity
            item.save()

            cart_item = CartItem.objects.filter(cart = cartdb)
            cart_quantity = 0
            for itm in cart_item:
                cart_quantity+=1

            cart_gst = (cartdb.total_item_price()) * 0.05

            cart_total = cartdb.total_item_price()

            if cartdb.coupon:
                cart_total -= cartdb.coupon_discount

            response = JsonResponse({'qty':cart_quantity, 'total':cart_total, 'gst':cart_gst})

            return response
        else:
            cart = Cart_session(request)

            variant_id = int(request.POST.get('variant_id'))
            product_quantity = int(request.POST.get('product_quantity'))

            cart.update(variant=variant_id, qty=product_quantity)
            cart_quantity = cart.__len__()

            cart_total = cart.get_total()

            cart_gst = cart.get_gst()


            response = JsonResponse({'qty':cart_quantity, 'total':cart_total, 'gst':cart_gst})

            return response



def add_coupon(request):

    if request.POST.get('action') == 'post':

        cartdb = Cart.objects.get(user = request.user, status = True)

        coupon_code =  request.POST.get('couponcode')
        
        # null checking
        if coupon_code == '':
            return JsonResponse({'status':False,'message':'got Null value'})

        try:
            coupon = Coupon.objects.get(name=coupon_code)
        except:
            return JsonResponse({'status':False,'message':'Entered coupon code either invalid or expired'})
        else:
            cart_total = cartdb.total_item_price()

            required_amount = coupon.min_amount
            discount_percent = coupon.off_percent
            max_discount = coupon.max_discount

            if cart_total >= required_amount:

                discount_price = (cart_total * discount_percent)/100


                if discount_price > max_discount:
                    discount_price = max_discount
                    applied_price = cart_total - discount_price

                
                    cartdb.coupon = coupon
                    cartdb.coupon_discount = discount_price
                    cartdb.save()
                    return JsonResponse({'message':f'coupon successfully added','couponcode':coupon_code,'total':cart_total-discount_price,'discount':discount_price,'grand_total':cart_total})
                else:
                    cartdb.coupon = coupon
                    cartdb.coupon_discount = discount_price
                    cartdb.save()
                    return JsonResponse({'message':F'coupon successfully added','couponcode':coupon_code,'total':cart_total-discount_price,'discount':discount_price,'grand_total':cart_total})

            else:
                return JsonResponse({'status':False,'message':F'Minimum purchase amount is {required_amount}'})

           

    return JsonResponse('success',safe=False)

def remove_coupon(request):

    if request.POST.get('action') == 'post':

        cartdb = Cart.objects.get(user = request.user, status = True)

        if cartdb.coupon:
            cartdb.coupon = None
            cartdb.coupon_discount = None
            cartdb.save()

            cart_total = cartdb.total_item_price()
            gst = cart_total * 0.05
            cart_total = cart_total + gst + 100

            return JsonResponse({'message':'coupon succefully removed','total': cart_total, 'gst':gst})
        else:
            return JsonResponse({'message':'something went wrong','status':False})

    return JsonResponse('success',safe=False)
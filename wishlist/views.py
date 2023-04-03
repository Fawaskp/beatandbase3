from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Wishlist
from admin_variant.models import Product_Variant
from django.contrib.auth.decorators import login_required

@login_required(login_url='user_login')
def wishlist(request):
    usr = request.user.id
    try:
        variants = Wishlist.objects.filter(user = usr)
    except:
        variants = ''  
    return render(request,'wishlist/wishlist.html',{'products':variants})

@login_required
def add_wishlist(request):
    variant_id = request.GET.get('id')
    user = request.user
    try:
        wishlist = Wishlist.objects.get(user=user, variant=variant_id)
    except Wishlist.DoesNotExist:
        variant = Product_Variant.objects.get(id=variant_id)
        wishlist = Wishlist(user=user,  variant=variant)
        wishlist.save()
    messages.success(request,'Item added to wishlist')
    return redirect('variant_detail', variant_id)

def delete_wishlist(request,variant_id):
    usr = request.user.id
    variant = Wishlist.objects.get(user = usr ,variant = variant_id)
    variant.delete()
    return redirect(wishlist)

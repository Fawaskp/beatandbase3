from .cart import Cart
from.models import Cart as Cart_db, CartItem

def cart(request):

    if request.user.is_authenticated:
        cart_db,_ = Cart_db.objects.get_or_create(user = request.user, status = True)
        cart_items = CartItem.objects.filter(cart=cart_db)
        cart_qty = 0
        if cart_items:
            for items in cart_items:
                cart_qty+=1
    else:
        cart = Cart(request)
        cart_qty = cart.__len__()
 
    return {'cart':Cart(request),'cart_qty':cart_qty}
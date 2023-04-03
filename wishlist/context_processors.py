from .models import Wishlist

def wishlist(request):
    usr = request.user.id

    val = 0
    try:
        for i in Wishlist.objects.filter(user = usr):
            val +=1 
    except:
        try:
            Wishlist.objects.get(user = usr)
            val = 1 
        except:
            val = 0
    return {'wishlist':val}
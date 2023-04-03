from django.shortcuts import render,redirect
from ad_banner.models import Advertisement
from admin_products import models as admin_products
from admin_products.models import Product_Image 
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from admin_variant.models import Product_Variant, Variant_images
from cart.models import Cart as Cart_db, CartItem
from django.db.models import Count,Avg
from django.contrib import messages
from .models import ReviewRating
from orders.models import Order_item

def user_products(request):

    # products = admin_products.Product.objects.all().order_by('product_name')
    variants = Product_Variant.objects.all()
 
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name_a_to_z':
        variants = variants.order_by('product__product_name')
    elif sort_by == 'name_z_to_a':
        variants = variants.order_by('-product__product_name')
    elif sort_by == 'price_low_to_high':
        variants = variants.order_by('price')
    elif sort_by == 'price_high_to_low':
        variants = variants.order_by('-price')
    
    # paginator = Paginator(products,6)
    # page_number = request.GET.get('page')
    # page_product = paginator.get_page(page_number)

    paginator = Paginator(variants,6)
    page_number = request.GET.get('page')
    page_variant = paginator.get_page(page_number)

    brand_ids = request.GET.getlist('brand')
    category_ids = request.GET.getlist('category')

    if brand_ids and category_ids:
        page_variant = variants.filter(product__brand__brand_id__in=brand_ids, product__category__in=category_ids)
    elif brand_ids:
        page_variant = variants.filter(product__brand__brand_id__in=brand_ids)
    elif category_ids:
        page_variant = variants.filter(product__category__in=category_ids)


    brands = admin_products.Brand.objects.annotate(product_count=Count('product'))
    categories = admin_products.Categories.objects.annotate(product_count=Count('product'))

    dicts = {
        'categories': categories,
        'brands': brands,
        'ad':Advertisement.objects.all().order_by('id'),
        # 'product':page_product,
        'variants':page_variant,
        'variant_images':Variant_images.objects.all()
    }
    return render(request,'user_products/user_variants.html',dicts)



def search_product(request):

    try:
        search_text = request.POST['search_text']
    except:
        return redirect(user_products)
    

    
    brand_ids = request.GET.getlist('brand')
    category_ids = request.GET.getlist('category')

    variants = Product_Variant.objects.filter(product__product_name__icontains=search_text)

    if brand_ids and category_ids:
        variants = variants.filter(product__brand__brand_id__in=brand_ids, product__category__in=category_ids, product__product_name__icontains=search_text)
    elif brand_ids:
        variants = variants.filter(product__brand__brand_id__in=brand_ids, product__product_name__icontains=search_text)
    elif category_ids:
        variants = variants.filter(product__category__in=category_ids, product__product_name__icontains=search_text)

    brands = admin_products.Brand.objects.annotate(product_count=Count('product'))
    categories = admin_products.Categories.objects.annotate(product_count=Count('product'))

    dicts = {
        'categories': categories,
        'brands': brands,
        'product':variants,
        'search_text' : search_text
    }
    return render(request,'user_products/product_search.html',dicts)

def product_detail(request,product_id):

    pro_images = ''
    try:
        mainproduct = admin_products.Product.objects.get(id=product_id)
    except:
        messages.error(request,'Sorry Product matching query does not exist')
        return redirect(user_products)
    
    # pro_category = main_product.category
    # pro_category
    pro_images = Product_Image.objects.filter(product=product_id)

    variants = Product_Variant.objects.filter(product=mainproduct)

    try:
        cartdb = Cart_db.objects.get(user = request.user,active = True)
    except:
        pass
    else:
        cart = CartItem.objects.get(cart = cartdb)

    dicts = {
        'variants':variants,
        'categories': admin_products.Categories.objects.all(),
        'ad':Advertisement.objects.all(),
        'm_product':mainproduct,
        'products':admin_products.Product.objects.all(),
        'checkout_qty':'checkout_qty',
        'images':pro_images,
        'variant_images':Variant_images.objects.filter(variant__in = variants),
        'cart':cart,
        'cartdb':cart,
    }
    return render(request,'user_products/detail.html',dicts)




def variant_detail(request,variant_id):
    pro_images = ''
    try:
        main_variant = Product_Variant.objects.get(id = variant_id)
    except:
        messages.error(request,'Sorry Product matching query does not exist')
        return redirect(user_products)
    # pro_category = main_product.category
    # pro_category
    variant_images = Variant_images.objects.filter(variant = variant_id)

    variants = Product_Variant.objects.filter(product=main_variant.product)

    try:
        cartdb = Cart_db.objects.get(user = request.user,status = True)
    except:
        cart = ''
    else:
        cart = CartItem.objects.filter(cart = cartdb)

    reveiws = ReviewRating.objects.filter(product = main_variant.product)
    try:
        is_ordered = Order_item.objects.filter(variant=main_variant, user=request.user).exists()
    except:
        is_ordered = False

    dicts = {
        'options':variants,
        'categories': admin_products.Categories.objects.all(),
        'ad':Advertisement.objects.all(),
        'm_variant':main_variant,
        'checkout_qty':'checkout_qty',
        'variants' : Product_Variant.objects.all(),
        'images':pro_images,
        'variant_images':Variant_images.objects.filter(variant__in = variants),
        'cart':cart,
        'reviews':reveiws,
        'total_reviews': reveiws.count(),
        'avg_rating' : reveiws.aggregate(Avg('rating'))['rating__avg'],
        'is_ordered' : is_ordered,
    }
    return render(request,'user_products/variant_detail.html',dicts)
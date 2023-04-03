from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product_Variant, Colors, Variant_images
from admin_products.models import Product
from django.http import JsonResponse
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator

def product_variants(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    variants= Product_Variant.objects.all().order_by('-product')

    paginator = Paginator(variants,5)
    page_number = request.GET.get('page')
    page_variant = paginator.get_page(page_number)

    context = {
        'variants' : page_variant,
        'products' : Product.objects.all().order_by('id'),
        'colors' : Colors.objects.all().order_by('id'),
    }
    return render(request,'admin_variant/product_variants.html',context)


def add_color(request):

    color = request.POST['color']
    Colors.objects.create(color_name = color)

    return redirect(product_variants)



def add_variant(request):
    product_id = request.POST['product']
    price = request.POST['price']
    color = request.POST['color']
    quantity = request.POST['quantity']

    # null value checking 
    check = [product_id,price,quantity]
    for values in check:
        if values == '':
            messages.info(request,'some fields are empty')
            return redirect(product_variants)
        else:
            pass

    # checking price and quantity is number
    try:
        check_number = int(price)
        check_number = int(quantity)
    except:
        messages.info(request,'number field got unexpected values')
        return redirect(product_variants)
    
    # checking price and quantity positive number
    check_pos =[int(price),int(quantity)]
    for value in check_pos:
        if value < 0:
            messages.info(request,'price and quantity should be positive number')
            return redirect(product_variants)
        else:
            pass
    
    try:
        image = request.FILES['image']
    except:
        image = ''
    
   
    product = Product.objects.get(id = product_id)
    color = Colors.objects.get(id=color)
    try:
        Product_Variant.objects.get(product=product,color=color)
    except:
        new = Product_Variant.objects.create(thumbnail=image, product=product,color=color, price=price, quantity=quantity)
        new.save()
    else:
        messages.info(request,f'{product} with {color} color already exist!')

    try:
        multiple_images = request.FILES.getlist('multiple_images')
        for image in multiple_images:
            image_model = Variant_images(variant = new, image=image)
            image_model.save()
    except:
        multiple_images = ''

    return redirect(product_variants)


def edit_variant(request,variant_id):
    product_id = request.POST['product']
    price = request.POST['price']
    color_id = request.POST['color']
    quantity = request.POST['quantity']

    check = [product_id,color_id,price,quantity]
    for values in check:
        if values == '':
            messages.info(request,'some fields are empty')
            return redirect(product_variants)
        else:
            pass
    
    try:
        check_number = int(price)
        check_number = int(quantity)
    except:
        messages.info(request,'number field got unexpected values')
        return redirect(product_variants)
    
    try:
        variant = Product_Variant.objects.get(id=variant_id)
        image = request.FILES['image']
        variant.thumbnail=image
        variant.save()
    except:
        pass
   
    product = Product.objects.get(id = product_id)
    color = Colors.objects.get(id=color_id) 
    variant = Product_Variant.objects.filter(id=variant_id)
    variant.update(product=product,color=color, price=price, quantity=quantity)

    try:
        multiple_images = request.FILES.getlist('multiple_images')
        variant = Product_Variant.objects.get(id=variant_id)
        for image in multiple_images:
            image_model = Variant_images(variant = variant, image=image)
            image_model.save()
    except:
        multiple_images = ''


    
    return redirect(product_variants)

def delete_variant(request):

    variant_id = request.GET.get('id')
    variant = Product_Variant.objects.get(id= variant_id)
    variant.delete()

    return redirect(product_variants)


def upload_images(request):
    if request.method == 'POST':
        var_id = request.GET.get('variant')
        variant = Product_Variant.objects.get(id=var_id)
        files = request.FILES.getlist('file')
        for file in files:
            image = Variant_images.objects.create(variant = variant, image=file)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

def search_variants(request):  
    search_text = request.POST['query']
    context = {
        'variants':Product_Variant.objects.filter(product__product_name__icontains=search_text),
        'search_text':search_text,
    }
    return render(request,'admin_variant/product_variants.html',context)


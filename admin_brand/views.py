from django.shortcuts import render,redirect
from .models import Brand 
from django.contrib import messages


def admin_brand(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    dict_brands = {
        'brands':Brand.objects.all().order_by('id')
    }
    return render(request,'admin_brand/admin_brand.html',dict_brands)

def add_brand(request):
    image = ''
    try:
        image = request.FILES['image']
    except:
        if image == '':
            messages.info(request,"Give field can't be empty")
            return redirect(admin_brand)
    name = request.POST['brand_name']
    if name == '':
        messages.info(request,"name field can't be empty")
        return redirect(admin_brand)
    # new = models.Product(
    #     product_img='null',
    #     product_name=name,
    #     product_price=price,
    #     product_quantity=quantity,
    #     brand=brand,
    #     category=category,
    # )
    # new.save()
    try:
        Brand.objects.get(brand_name=name)
    except:
        new = Brand.objects.create(brand_name=name,brand_img=image)
        new.save()
    else:
        messages.error(request,f'Brand "{name}" already exist')
        return redirect(admin_brand)
    messages.success(request,f'Created Brand "{name}" Successfully')
    return redirect(admin_brand)

def edit_brand(request,brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        image = request.FILES['image']
        brand.brand_img = image
        brand.save()
    except:
        pass
    
    name = request.POST['brand_name']
    brand = Brand.objects.get(id = brand_id)

    try:
        if not brand.brand_name == name:
            value = Brand.objects.get(brand_name = name)
        else:
            return redirect(admin_brand)
    except:
        brand.brand_name = name
        brand.save()
    else:
        messages.info(request,f'brand_name {name} already exist')
        return redirect(admin_brand)
        
    return redirect(admin_brand)

def delete_brand(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    brand.delete()
    messages.info(request,f'deleted brand {brand.brand_name}')
    return redirect(admin_brand)


def search_brands(request):  
    search_text = request.POST['query']
    context = {
        'brands':Brand.objects.filter(brand_name__icontains=search_text),
        'search_text':search_text,
    }
    return render(request,'admin_brand/admin_brand.html',context)
from django.shortcuts import render,redirect
from .models import Product, Product_Image
from admin_brand.models import Brand
from admin_category.models import Categories
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator


def admin_products(request):

    products = Product.objects.all().order_by('id')

    paginator = Paginator(products,3)
    page_number = request.GET.get('page')
    page_product = paginator.get_page(page_number)

    context = {
        'products':page_product,
        'categories':Categories.objects.all(),
        'brands':Brand.objects.all(),
    }
    return render(request,'admin_products/admin_products.html',context)

def add_product(request):
    name = request.POST['product_name']
    brand = request.POST['product_brand']
    category = request.POST['product_category']
    description = request.POST['description']

    check = [name,brand,category]
    for values in check:
        if values == '':
            messages.info(request,'some fields are empty')
            return redirect(admin_products)
        else:
            pass
    
    
    brand_instance = Brand.objects.get(id=brand)
    category_instance = Categories.objects.get(id=category)
    new = Product.objects.create(product_name=name,brand=brand_instance,category=category_instance,product_description=description)
    new.save()
    messages.success(request,f'Product {name} created succefully')
    return redirect(admin_products)



def edit_product(request,product_id):
    name = request.POST['product_name']
    brand = request.POST['product_brand']
    category = request.POST['product_category']

    if name == '':
        messages.error(request,"Product name can't be null")
        return redirect(admin_products)

    
    brand_instance = Brand.objects.get(id=brand)
    category_instance = Categories.objects.get(id=category)
    product = Product.objects.filter(id=product_id).update(product_name=name,brand=brand_instance,category=category_instance)
    mess_status = True
    messages.success(request,f'{name} updated successfully')
    return redirect(admin_products)

def delete_product(request,product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.info(request,f'deleted product "{product.product_name}"')
    return redirect(admin_products)


def search_product(request):  
    search_text = request.POST['query']
    context = {
        'products':Product.objects.filter(product_name__icontains=search_text),
        'categories':Categories.objects.all(),
        'brands':Brand.objects.all(),
        'search_text':search_text,
    }
    return render(request,'admin_products/admin_products.html',context)
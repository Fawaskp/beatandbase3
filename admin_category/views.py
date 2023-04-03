from django.shortcuts import render,redirect
from .models import Categories
from django.contrib import messages


def admin_category(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    dict_category = {
        'categories':Categories.objects.all()
    }
    return render(request,'admin_category/admin_category.html',dict_category)

def add_category(request):
    image = ''
    try:
        image = request.FILES['image']
    except:
        if image == '':
            messages.info(request,"Image field can't be empty")
            return redirect(admin_category)
    name = request.POST['category_name']
    if name == '':
        messages.info(request,"category name can't be empty ")
        return redirect(admin_category)
    
    try:
        Categories.objects.get(category_name = name)
    except:
        Categories.objects.create(category_name=name,category_image=image).save()
    else:
        messages.error(request,f'Category "{name}" already exist')
        return redirect(admin_category)
    messages.success(request,f'Created Brand "{name}" Successfully')
    return redirect(admin_category)

def edit_category(request,category_id):
    try:
        category = Categories.objects.get(id=category_id)
        image = request.FILES['image']
        category.category_image = image
        category.save()
    except:
        pass

    name = request.POST['category_name']

    if name == '':
        messages.error(request,"category name can't be null")
        return redirect(admin_category)

    category = Categories.objects.filter(id=category_id)
    category.update(category_name=name)
    return redirect(admin_category)

def delete_category(request,category_id):
    category = Categories.objects.get(id=category_id)
    category.delete()
    messages.info(request,f'deleted category {category.category_name}')
    return redirect(admin_category)


def error_404(request, exception):
    return render(request, '404.html', status=404)
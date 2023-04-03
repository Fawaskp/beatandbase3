from django.shortcuts import render,redirect
from ad_banner.models import Advertisement
from admin_brand.models import Brand

def ad_banner(request):
    dict_ad = {
        'ad':Advertisement.objects.all().order_by('id'),
        'brands': Brand.objects.all()
    }
    return render(request,'ad_banner/ad_banner.html',dict_ad)

def add_ad(request):
    try:
        image = request.FILES['image']
    except:
        pass
    brand = request.POST['brand_name']
    brand_instance = Brand.objects.get(id=brand)
    Advertisement.objects.create(brand=brand_instance,ad_image=image).save()

    return redirect(ad_banner)

def edit_ad(request,ad_id):
    ad = Advertisement.objects.get(id=ad_id)
    brand = request.POST['brand_name']
    brand_instance = Brand.objects.get(id = brand)
    try:
        image = request.FILES['image']
        ad.ad_image = image
        ad.save()
    except:
        pass
    ad.brand = brand_instance
    ad.save()
    return redirect(ad_banner)

def delete_ad(request,ad_id):
    ad = Advertisement.objects.get(id=ad_id).delete()
    return redirect(ad_banner)

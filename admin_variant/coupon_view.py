from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product_Variant
from .models import Coupon

def admin_coupon(request):
    context = {
        'coupons' : Coupon.objects.all()
    }
    return render(request,'admin_home/admin_offers.html',context)


def add_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        min_amount = request.POST.get('min_amount')
        discount_percent = request.POST.get('discount_percent')
        max_discount = request.POST.get('max_discount')
        count = request.POST.get('count')
        expire = request.POST.get('expire_date')
        active_status = request.POST.get('active_status')

        null_check = [
            coupon_name,min_amount,discount_percent,
            max_discount,count,expire,active_status
        ] 

        for val in  null_check:
            if val == '':
                messages.success(request,f'Some fields are empty')
                return redirect(admin_coupon)
        
        num_check = [
            min_amount,discount_percent,max_discount,count
        ]

        try:
            for num in num_check:
                num = int(num)
                if num < 0:
                    messages.success(request,f'Integer field should be positive')
                    return redirect(admin_coupon)
        except:
            messages.success(request,f'Integer field got unexpected values')
            return redirect(admin_coupon)
        


        if active_status == 'on':
            active_status = True
        else:
            active_status = False
            
        try:
            Coupon.objects.get(name = coupon_name)
        except:
            pass
        else:
            messages.success(request,f'Coupon name already exist')
            return redirect(admin_coupon)

        Coupon.objects.create(
            name=coupon_name,
            min_amount=min_amount, 
            off_percent=discount_percent, 
            max_discount=max_discount,
            expiry_date=expire,
            quantity=count,
            status=active_status,
            )
        messages.success(request,f'{coupon_name} created successfully')
        return redirect(admin_coupon)
    else:
        return redirect(admin_coupon)
    

def delete_coupon(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        print('coupon id = ',coupon_id)
        try:
            coupon = Coupon.objects.get(id = coupon_id)
            coupon.delete()
            messages.success(request,f'deleted {coupon} successfully')
            return redirect(admin_coupon)
        except:
            return redirect(admin_coupon)
    else:
        messages.error(request,f'something went wrong')
        return redirect(admin_coupon)
    
def edit_coupon(request):

    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        min_amount = request.POST.get('min_amount')
        discount_percent = request.POST.get('discount_percent')
        max_discount = request.POST.get('max_discount')
        count = request.POST.get('count')
        expire = request.POST.get('expire_date')
        active_status = request.POST.get('active_status')
        coupon_id = request.POST.get('coupon_id')

        null_check = [
            coupon_name,min_amount,discount_percent,
            max_discount,count,expire,active_status
        ] 

        for val in  null_check:
            if val == '':
                messages.success(request,f'Some fields are empty')
                return redirect(admin_coupon)
        
        num_check = [
            min_amount,discount_percent,max_discount,count
        ]

        try:
            for num in num_check:
                num = int(num)
                if num < 0:
                    messages.success(request,f'Integer field should be positive')
                    return redirect(admin_coupon)
        except:
            messages.success(request,f'Integer field got unexpected values')
            return redirect(admin_coupon)
        
        if active_status == 'on':
            active_status = True
        else:
            active_status = False
        coupon = Coupon.objects.filter(id =  coupon_id)
        coupon.update(
            name=coupon_name,
            min_amount=min_amount, 
            off_percent=discount_percent, 
            max_discount=max_discount,
            quantity=count,
            status=active_status,
            )
        if expire:
            coupon.update(expiry_date=expire)
        messages.success(request,f'{coupon_name} edited successfully')

        return redirect(add_coupon)
    
    else:
        messages.error(request,f'something went wrong')
        return redirect(admin_coupon)
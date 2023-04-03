from django.shortcuts import render,redirect
from django.contrib import messages,auth
from user_home.models import CustomUser, UserOTP,Mobile_Otp
from admin_products import models as admin_products
from admin_variant.models import Product_Variant
from admin_brand.models import Brand
from ad_banner.models import Advertisement
from django.core.mail import send_mail
from django.conf import settings
from . import mixin
import random
from django.core.exceptions import ValidationError
import re


def validateEmail( email ):
    from django.core.validators import validate_email
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    

def validate_name(value):
    
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    else:
        return False
    
            

def index(request):
    
    context = {
        'ad':Advertisement.objects.all(),
        'variants':Product_Variant.objects.all().order_by('-id')[:8],
        'product':admin_products.Product.objects.all().order_by('-id'),
        'brands':Brand.objects.all(),
        }
    
    return render(request,'user_home/index.html',context)


def user_register(request):

    """ OTP VERIFICATION """

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=CustomUser.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect(user_login)
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'user_home/user_register.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:    
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password1 = request.POST['pass1']
            password2 = request.POST['pass2']
            
            # null values checking
            check = [name,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'user_home/user_register.html',context)
                else:
                    pass

            result = validate_name(name)
            if result is not False:
                context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,result)
                return render(request,'user_home/user_register.html',context)
            else:
                pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'user_home/user_register.html',context)
            else:
                pass
            
            try:
                check_number = int(mobile)
                if len(mobile) <10 :
                    raise Exception
            except:
                context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid Mobile number')
                return render(request,'user_home/user_register.html',context)
            
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter Strong Password')
                return render(request,'user_home/user_register.html',context)
            else:
                pass
            if password1 == password2:
                try:
                    CustomUser.objects.get(phone=mobile)
                except:
                    pass
                else:
                    context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'Mobile number is already registered')
                    return render(request,'user_home/user_register.html',context)
                try:
                    CustomUser.objects.get(email=email)
                except:
                    usr = CustomUser.objects.create_user(username=name,email=email,phone=mobile,password=password1)
                    usr.is_active=False
                    usr.save()
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for beatandbase is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to Beatandbase Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request,'user_home/user_register.html',{'otp':True,'usr':usr})
                else:
                    context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'user alreadt exist')
                    return render(request,'user_home/user_register.html',context)
            else:
                context ={
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.error(request,'password mismatch')
                return render(request,'user_home/user_register.html',context)
    else:
        return render(request,'user_home/user_register.html')

def user_login(request):
    get_otp=request.POST.get('otp')
    if get_otp:
            get_email=request.POST.get('email')
            usr=CustomUser.objects.get(email=get_email)
            try:
                int(get_otp)
            except:
                messages.error(request,'enter valid otp')
                return render(request,'user_home/user_register.html',{'otp':True,'usr':usr})
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'You accout is activated now{usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect(user_login)
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'user_home/user_register.html',{'otp':True,'usr':usr})
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if email == '':
            messages.info(request,'some fields is empty')
            return redirect(user_login)
        elif password == '':
            messages.info(request,'some fields is empty')
            return redirect(user_login)
        
        try:
            CustomUser.objects.get(email=email)
        except:
            messages.info(request,'No account found')
            return redirect(user_login)

        if not CustomUser.objects.get(email=email).is_active:
            usr = CustomUser.objects.get(email=email)
            user_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=usr,otp=user_otp)
            mess=f'Hello\t{usr.username},\nYour OTP to verify your account for beatandbase is {user_otp}\nThanks!'
            send_mail(
                    "welcome to Beatandbase Verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                )
            messages.info(request,'account not verified')
            return render(request,'user_home/user_register.html',{'otp':True,'usr':usr})
        else:
            if CustomUser.objects.get(email=email).is_blocked:
                messages.info(request,"Your account is blocked, Please try later")
                return redirect(user_login)
       
        if user is not None:
            auth.login(request,user)
            return redirect(index)              
        else:
            messages.info(request,'credential mismatch')
            return redirect(user_login)
    else:
        return render(request,'user_home/user_login.html')

def user_logout(request):
    auth.logout(request)
    return redirect(user_login)

def categories(request):
    dict_category = {
        'categories': admin_products.Categories.objects.all(),
        'ad':Advertisement.objects.all(),
    }
    return render(request,'user_home/categories.html',dict_category)


def mobile_login(request):
    if request.method == 'POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=CustomUser.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Account is created for {usr.email}')
                return redirect(user_login)
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'user_home/user_register.html',{'otp':True,'usr':usr})
        mobile = request.POST['mobile']
        user = request.user
        otp = random.randint(100000,999999)
        c_mobile = '+91'+mobile
        try:
            CustomUser.objects.filter(phone=int(mobile))
        except:
            messages.error(request,'Entered mobile number is not registered')
            return redirect(mobile_login)
        try:
            mixin.send_otp_on_phone(c_mobile,otp)
            Mobile_Otp.objects.create(user=user,otp=otp)
            return render(request,'user_home/user_login.html',{'otp':True,'user':user})
        except:
            messages.error(request,f"unable to send otp to registered number {mobile}")
            return redirect(mobile_login)

    else:
        return render(request,'user_home/user_mobile_login.html')


def forgot_password(request):
    if request.method == 'POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=CustomUser.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Now you can reset your password {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return render(request, 'user_home/reset_password.html',{'user':usr})
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request, 'user_home/forgot_password.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            email = request.POST.get('email')
            if CustomUser.objects.filter(email=email).exists():
                usr = CustomUser.objects.get(email__exact=email)
                user_otp=random.randint(1000,9999)
                UserOTP.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to forgot password is {user_otp}\nThanks!'
                send_mail(
                        "welcome to Beatandbase Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                messages.success(request, 'OTP sent to you email')
                return render(request, 'user_home/forgot_password.html',{'otp':True,'usr':usr})

            else:
                messages.error(request, 'Account does not exist!')
                return redirect('forgot_password')
    return render(request, 'user_home/forgot_password.html')


from django.core.exceptions import ValidationError

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

    
def reset_password(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = request.POST.get('fjkha67UTAnh?"}[njkGTFCXD#A@!21^^*87ghjuguy67')
            user = CustomUser.objects.get(id=user)
            Pass = ValidatePassword(password)
            if Pass is False:
                messages.success(request, 'Enter Strong password')
                message = 'Enter Strong password'
                return redirect('reset_password')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset succesfull')
            return redirect(user_login)
        else:
            messages.error(request, 'Password doesnot match')
            return redirect('reset_password')

    return render(request, 'user_home/reset_password.html')

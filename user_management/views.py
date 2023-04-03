from django.shortcuts import render,redirect
from user_home.models import CustomUser
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings

def user_list(request):

    users = CustomUser.objects.all().order_by('id')

    paginator = Paginator(users,5)
    page_number = request.GET.get('page')
    page_user = paginator.get_page(page_number)

    dict_user = {
        'users':page_user,
    }
    return render(request,'user_management/user_list.html',dict_user)


def user_action(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    if user.is_blocked:
        user.is_blocked=False
        user.save()
        mess=f'''Hello\t{user.username}, Your blocked beatandbase account has been unblocked
        '''
        send_mail(
                "Unblocked your account",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        return redirect(user_list)
    else:
        user.is_blocked=True
        mess=f'''Hello\t{user.username}, For your kind information your beatandbase account is blocked
        '''
        send_mail(
                "You account is blocked!",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        user.save()
        return redirect(user_list)
    

def search_users(request):  
    search_text = request.POST['query']
    context = {
        'users':CustomUser.objects.filter(username__icontains=search_text),
        'search_text':search_text,
    }
    return render(request,'user_management/user_list.html',context)
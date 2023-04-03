from django.shortcuts import render,redirect
from django.contrib import messages,auth
from orders.models import Order, Order_item
from user_home.models import CustomUser
from orders.models import Order_item
from django.db.models import Sum, DateField
from admin_variant.models import Product_Variant
from django.http import JsonResponse
from user_products.models import ReviewRating
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay, Cast
from django.core.paginator import Paginator


def admin_login(request):
    if request.user.is_superuser:
        return redirect(admin_home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect(admin_home)
            else:
                messages.error(request,f"{user} is not have admin access")
                return redirect(admin_login)
        else:
            messages.info(request,'credential mismatch')
            return redirect(admin_login)
    else:
        return render(request,'admin_home/admin_login.html')

def admin_logout(request):
    auth.logout(request)
    return redirect(admin_login)



def admin_home(request):
    if not request.user.is_superuser:
        return redirect(admin_login)

    delivered_item = Order_item.objects.filter(status='delivered')

    revenue = 0
    for item in delivered_item:
        revenue+=item.get_total()

    top_selling = Order_item.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = Order_item.objects.all().order_by('-id')[:5]


    # Getting the current date
    today = datetime.today()
    date_range = 7

    # Get the date 7 days ago
    four_days_ago = today - timedelta(days=date_range)

    #filter orders based on the date range
    orders = Order.objects.filter(placed_at__gte=four_days_ago, placed_at__lte=today)

    # Getting the sales amount per day
    sales_by_day = orders.annotate(day=TruncDay('placed_at')).values('day').annotate(total_sales=Sum('total')).order_by('day')

    # Getting the dates which sales happpened
    sales_dates = Order.objects.annotate(sale_date=Cast('placed_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':CustomUser.objects.count(),
        'sales':Order_item.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    
    return render(request,'admin_home/admin_home.html',context)


def admin_orders(request): 
    if not request.user.is_superuser:
        return redirect(admin_login)

    orders = Order.objects.all().order_by('-id')

    paginator = Paginator(orders,5)
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)

    context = {
        'orders' : page_orders,
        'items' : Order_item.objects.all(),
        'status_choices' : dict(Order_item.ORDER_STATUS_CHOICES)
    }
    return render(request,'admin_home/admin_orders.html', context)

def admin_review(request): 
    if not request.user.is_superuser:
        return redirect(admin_login)
    
    context = {
        'reviews':ReviewRating.objects.all()
    }

    return render(request,'admin_home/admin_reviews.html',context)

def review_delete(request):
    if not request.user.is_superuser:
        return redirect(admin_login)
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        try:
            review = ReviewRating.objects.get(id=review_id)
            review.delete()
        except:
            messages.error(request,'something went wrong')
            return redirect(admin_review)

    messages.success(request,f'Successfull deleted the review {review.review}')
    return redirect(admin_review)


def change_order_status(request):
    item_id = request.POST.get('item_id')
    value = request.POST.get('status')

    item = Order_item.objects.get(id=item_id)
    item.status = value
    item.save()
    return JsonResponse('success',safe=False)


def admin_sales(request):
    if not request.user.is_superuser:
        return redirect(admin_login)
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(admin_sales)
        
        if start_date ==  end_date :
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = Order_item.objects.filter(order__placed_at__date=date_obj.date())
            if order_items:
                context.update(sales = order_items,s_date=start_date,e_date = end_date)
                return render(request,'admin_home/admin_sales.html',context)
            else:
                messages.error(request,'no data found')
            return redirect(admin_sales)

        order_items = Order_item.objects.filter(order__placed_at__gte=start_date, order__placed_at__lte=end_date)

        if order_items:
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')

    return render(request,'admin_home/admin_sales.html',context)

def admin_profile(request):
    return render(request,'admin_home/admin_profile.html')
    
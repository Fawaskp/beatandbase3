from .forms import ReviewForm,ReviewRating
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin_variant.models import Product_Variant


def submit_review(request):
    if request.method == 'POST':

        variant_id = request.POST.get('variant_id') 
        if variant_id:
            try:
                variant = Product_Variant.objects.filter(id = variant_id)
                product_id = variant[0].product.id
            except:
                messages.error(request, 'Review product not not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)  # Checks whether the review of the product by the user exists.
                                                              # If exists, it will detect that review needs to be updated.
                                                              # Else save it as a new review
                                                              # If instance not passed, it will save it as a new review
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            
            if form.is_valid():
                data = ReviewRating()
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.user = request.user
                data.product_id = product_id
                data.save()
                messages.success(request, 'Thank you! Your review have been saved.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
    messages.error(request, 'Not success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
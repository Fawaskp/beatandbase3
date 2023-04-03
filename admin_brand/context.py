from .models import Brand

def brand_context(request):
    context = {
        'brands' : Brand.objects.all()
        }
    return context
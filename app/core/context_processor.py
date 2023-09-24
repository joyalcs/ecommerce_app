from core.models import Category

def custom_context(request):
    categories = Category.objects.all()

    return {
        'categories':categories
    }


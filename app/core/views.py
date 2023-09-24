from django.shortcuts import render
from django.views import View
from .models import Product, Category

# Create your views here.

class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        context ={
            'products':products,
            'categories':categories,
        }
        return render(request, 'core/home.html', context)

class Category_product_list_view(View):
    def get(self, request, cid):
        category = Category.objects.get(cid=cid)
        products = Product.objects.filter(category=category)

        context = {
            'category':category,
            'products':products
        }
        return render(request, 'core/category-list.html', context)


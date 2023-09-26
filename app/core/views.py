from django.shortcuts import render
from django.views import View
from .models import Product, Category, ProductReview
from django.core.cache import cache
from .forms import ProductReviewForm
from django.http import JsonResponse
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
        try:
            category = Category.objects.get(cid=cid)
        except Category.DoesNotExist:
            category = None
        products = Product.objects.filter(category=category)

        context = {
            'category':category,
            'products':products
        }
        return render(request, 'core/category-list.html', context)


class All_Product_list_view(View):
    def get(self, request):
        products = Product.objects.all()
        context = {
            'products':products
        }
        return render(request, 'core/all_products.html', context)


class Single_product_view(View):
    def get(self, request, pid):
        try:
            product = Product.objects.get(pid=pid)

        except Product.DoesNotExist:
            product = None
        review_form = ProductReviewForm()
        p_image = product.p_images.all()
        products = Product.objects.filter(category=product.category).exclude(pid=pid)
        reviews = ProductReview.objects.filter(product=product)
        context = {
            'product' : product,
            'p_image':p_image,
            'products': products,
            'reviews': reviews,
            'review_form':review_form,
        }

        return render(request, 'core/product-detail.html', context)
    def post(self, request, pid):
        review_form = ProductReviewForm(request.POST)
        post= ProductReview.objects.get(pid=pid)
        if review_form.is_valid():
            review = review_form.save()
            review.post=post
            review.save()


def AjaxAddReviewView(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
    )

    context = {
        'user':user.username,
        'review':request.POST['review'],
    }
    return JsonResponse({
        'bool': True, 'context':context, })




from django.shortcuts import render
from django.views import View
from .models import Product, Category, ProductReview
from django.core.cache import cache
from .forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Min, Max
from django.shortcuts import redirect
# Create your views here.

# View for home page
class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        context ={
            'products':products,
            'categories':categories,
        }
        return render(request, 'core/home.html', context)

#View for category
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


#View for all product
class All_Product_list_view(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
        context = {
            'products':products,
            'categories':categories,
            'min_max_price': min_max_price,
        }
        return render(request, 'core/all_products.html', context)


#View for detailed view for a single product
class Single_product_view(View):
    def get(self, request, pid):
        try:
            product = Product.objects.get(pid=pid)

        except Product.DoesNotExist:
            product = None
        review_form = ProductReviewForm()
        products = Product.objects.filter(category=product.category).exclude(pid=pid)
        reviews = ProductReview.objects.filter(product=product).order_by("-date")
        context = {
            'product' : product,
            'products': products,#related products
            'reviews': reviews,
            'review_form':review_form,
        }

        return render(request, 'core/product-detail.html', context)


#View for adding review
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


#View for searching products
def SearchView(request):
    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(title__icontains=query).order_by("-date")
    else:
        products=[]
    context = {
        'products':products,
        'query':query
    }
    return render(request, 'core/search.html', context)

# View for filter products with price using slider
def FilterProductView(request):
    categories = request.GET.getlist("category[]")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    if min_price is not None and min_price.isdigit():
        products = products.filter(price__gte=min_price)
    if max_price is not None and max_price.isdigit():
        products = products.filter(price__lte=max_price)
    if len(categories)>0:
        products = products.filter(category__id__in=categories).distinct()

    data = render_to_string('core/async/products.html', {'products': products})
    return JsonResponse({'data':data})


# View for Adding items to the cart

def Add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])]={
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], "totalcartitems":len(request.session['cart_data_obj'])})


# View for viewing cart page

def cart_items(request):
    cart_total_price = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_price += int(item['qty']) * float(item['price'])
        return render(request, 'core/cart.html', {"data":request.session['cart_data_obj'], "totalcartitems":len(request.session['cart_data_obj']), "cart_total_price": cart_total_price} )
    else:
        return redirect('core:home')



# View for deleting items in the cart

def cart_items_delete(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_price = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_price += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"data":request.session['cart_data_obj'], "totalcartitems":len(request.session['cart_data_obj']), "cart_total_price": cart_total_price})
    return JsonResponse({"data":context, "totalcartitems":len(request.session['cart_data_obj'])})

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'
urlpatterns = [
    #Home
    path('', views.HomeView.as_view(), name='home'),

    # Category
    path('category/<cid>/', views.Category_product_list_view.as_view(), name='category-list'),

    #Products
    path('products/', views.All_Product_list_view.as_view(), name="product-list"),
    path('product/<pid>/', views.Single_product_view.as_view(), name='single-product'),
    path('review/<pid>/', views.AjaxAddReviewView, name='review'),
    path('search/', views.SearchView, name='search'),
    path('filter-products/', views.FilterProductView, name='filter-products'),
    path('add-to-cart/', views.Add_to_cart, name="add-to_cart"),
    path('cart/', views.cart_items, name="cart-items"),
    path('delete-product-from-cart/', views.cart_items_delete, name="delete-product-from-cart")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

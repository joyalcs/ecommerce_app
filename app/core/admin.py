from django.contrib import admin
from .models import Category,Vendor, ProductImages,Product, CartOrder, CartOrderItems, ProductReview, Wishlist, Address


class CatgoryAdmin(admin.ModelAdmin):
    list_display=['title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display=['user', 'title', 'product_image', 'price', 'featured', 'product_status']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display=['order', 'item', 'image', 'invoice_no', 'product_status', 'qty', 'total_price']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating', 'date']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']

admin.site.register(Category, CatgoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)




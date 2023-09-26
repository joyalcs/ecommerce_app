from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from user.models import User
# Create your models here.
STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)
STATUS_CHOICE = (
    ("process", "processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

def user_directory_path(instance, filename):
    return f'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat")
    title = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven")
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(max_length=250)
    address = models.TextField(max_length=250)
    contact = models.CharField(max_length=13, default='+91')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.title

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="pro", alphabet="abcdefgh123456")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    specifications = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(max_digits=6, decimal_places=2)
    product_status = models.CharField(choices=STATUS, default="In Review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.BooleanField(default=False)

    def get_percentage(self):
        new_price = (self.price/self.old_price) * 100
        return 100-new_price

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.title} - ${self.price} - {self.status}"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"
####################################################

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE)

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(choices=STATUS_CHOICE)
    item = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    invoice_no = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'% (self.image))

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Review"

    def get_rating(self):
        return self.rating

    def __str__(self):
        return self.product.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=200)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

    def __str__(self):
        return f'{self.user}, {self.address}'

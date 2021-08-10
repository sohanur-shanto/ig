from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=220)
    number = models.CharField(max_length=11, blank=True, null=True)
    company = models.CharField(max_length=220)


    def __str__(self):
        return self.company


class Category(models.Model):
    name = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    image = models.ImageField(null=True, blank=True)
    brand = models.CharField(max_length=220, null=True, blank=True)
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.TextField(max_length=10000)
    rating = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    old_price = models.DecimalField(max_digits=11, decimal_places=2)
    discount = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    countInStock = models.IntegerField(blank=True, null=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)


    def save(self, *args, **kwargs):
        self.price = Decimal(self.old_price * (100 - self.discount) / 100)
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=220, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)



class Order(models.Model):

    PENDING_PAYMENT = 'PENDING_PAYMENT'
    status_choices = [

        ('CANCEL', 'Cancel'),
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('ON_HOLD', 'On Hold'),
        ('WAITING_FOR_PAYMENT', 'Waiting For Payment'),
        ('PROCESSING', 'Processing'),
        ('COMPLETE', 'Complete'),

    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliverAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=220, choices=status_choices, default=PENDING_PAYMENT)
    _id = models.AutoField(primary_key=True, editable=False)


    def __str__(self):
        return self._id



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name



class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=220, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.address

    





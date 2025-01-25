from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name  = models.CharField(max_length=200, null=True)
    email  = models.EmailField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.CharField(null=True, blank = True)
    description = models.CharField(null = True, blank=True)
    rating = models.PositiveIntegerField("default = 0")

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def star_rating(self):
        # returns a list representing the star rating in the back for the frontend use
        return [False] * self.rating + [True] * (5 - self.rating)
        

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')],
        default='Pending',
    )


    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

    # this loops through the cart item of a user to know if the selected product is a digital or physical item, 
    # if it is a physical item no need for shipping but if it is digital, ship it
     
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null =  True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __Str__ (self):
        return self.product.name
    
    # to calculate the total in the cart of a user
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True, null = True)
    #
    # date_added = models.CharField(max_length=200, null=False)


    class Meta:
        verbose_name_plural = "Shipping Address"  


    def __str__(self):
        return f"{self.address} - {self.date_added.strftime('%Y-%m-%d %H:%M:%S')}"

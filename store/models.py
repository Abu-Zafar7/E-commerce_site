from django.db import models

from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User,on_delete= models.CASCADE, null= True, blank= True)
    name = models.CharField(max_length=100, null= True, blank= True)
    email = models.EmailField(blank= True, null= True)
    phone_number = models.CharField(max_length=10, null= True, blank= True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=100, null= True, blank= True)
    description = models.TextField(blank= True, null= True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to= 'products/', blank= True, null= True)
    status = models.CharField(choices=[('Pending','Pending'), ('Completed','Completed')], max_length=10, default= "Pending")

    def __str__(self) -> str:
        return self.name


    @property
    def imageURL(self):

        try: 
            url = self.image.url

        except:
            url = ""         

        return url    
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=10, default="Pending")
    transaction_id = models.CharField(max_length=100, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)  # New field for Razorpay order ID

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.status == "Pending":
                shipping = True
        return shipping

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



class OrderItem(models.Model):

    product = models.ForeignKey(Product, related_name='items', on_delete=models.SET_NULL,  blank= True, null= True)
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null= True)
    quantity = models.IntegerField(default=0, null= True, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Shipping(models.Model):

    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, blank=True, null= True)  
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address

    


        
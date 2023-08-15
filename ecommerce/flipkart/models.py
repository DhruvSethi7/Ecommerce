from django.db import models

# Create your models here.
class product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    product_desc=models.CharField(max_length=300)
    product_price=models.IntegerField(default=0)
    catergory=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    pub_date=models.DateField()
    image=models.ImageField(upload_to='flipkart/images',default='')
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class OrderStatus(models.TextChoices):
    PENDING = 'Pending'
    PAID = 'Paid'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=10, unique=True)  # Ensuring the order_id is unique.
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    amount = models.IntegerField(default=0)
    items_json = models.TextField()  # A TextField might be more suitable for storing long JSON strings.
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=254)  # Use EmailField for email validation.
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=50, blank=True)
class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)
    def __str__(self):
     return self.update_desc[0:7] + "..."
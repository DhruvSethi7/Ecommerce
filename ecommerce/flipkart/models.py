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


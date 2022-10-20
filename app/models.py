
from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.core.exceptions import ValidationError
import re
from app.modelmanager import CustomUserManager


def mobile_validate(value):
    val = re.fullmatch("[7-9]\d{9}",value)
    if val == None:
        raise ValidationError("Enter valid mobile number. should startwith(7,8,9) and contain 10digits")

STATE_CHOICES = (
  ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
  ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
  ('Assam','Assam'),
  ('Bihar','Bihar'),
  ('Chandigarh','Chandigarh'),
  ('Chhattisgarh','Chhattisgarh'),
  ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
  ('Daman and Diu','Daman and Diu'),
  ('Delhi','Delhi'),
  ('Goa','Goa'),
  ('Gujarat','Gujarat'),
  ('Haryana','Haryana'),
  ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu & Kashmir','Jammu & Kashmir'),
  ('Jharkhand','Jharkhand'),
  ('Karnataka','Karnataka'),
  ('Kerala','Kerala'),
  ('Lakshadweep','Lakshadweep'),
  ('Madhya Pradesh','Madhya Pradesh'),
  ('Maharashtra','Maharashtra'),
  ('Manipur','Manipur'),
  ('Meghalaya','Meghalaya'),
  ('Mizoram','Mizoram'),
  ('Nagaland','Nagaland'),
  ('Odisha','Odisha'),
  ('Puducherry','Puducherry'),
  ('Punjab','Punjab'),
  ('Rajasthan','Rajasthan'),
  ('Sikkim','Sikkim'),
  ('Tamil Nadu','Tamil Nadu'),
  ('Telangana','Telangana'),
  ('Tripura','Tripura'),
  ('Uttarakhand','Uttarakhand'),
  ('Uttar Pradesh','Uttar Pradesh'),
  ('West Bengal','West Bengal'),
)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    mobile_no = models.CharField(null= True,blank=False,max_length=10,unique=True, validators=[mobile_validate])
    email = models.EmailField(_('email address'), unique=True)
    address = models.CharField(max_length=200,blank=False )
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField(null= True,blank=False,max_length=5)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile_no = mobile_no = models.CharField(null= True,blank=False,max_length=10,unique=True, validators=[mobile_validate])
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

PRODUCT_CHOICES = (
    ("jeans","Jeans" ),
    ("t-shirts", "T-Shirts"),
    ("shirts", "Shirts"),
    ("saree", "Saree"),
    ("kurtas", "Kurtas"),
    ("mobile", "Mobile"),
    ("laptop","Laptop"),
)

class Product(models.Model):
    
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    category = models.CharField(choices=PRODUCT_CHOICES, max_length=20)
    brand = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to="product_img")

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return str(self.id)

STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Canceled','Cancel')
)

class Product_Status(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=25, default="Pending")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price









   
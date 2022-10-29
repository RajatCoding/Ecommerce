from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def add_create(sender, instance, created, raw, using, update_fields,**kwargs):
      if created:
            city = instance.city
            state = instance.state
            address = instance.address
            zipcode = instance.zipcode
            first_name = instance.first_name
            last_name = instance.last_name
            mobile_no = instance.mobile_no
            Customer(name = first_name+ " "+last_name, mobile_no = mobile_no,state=state, city=city, locality=address, zipcode=zipcode, user = instance, user_address=True).save()
            print("done")
 
@receiver(post_save, sender=User)
def add_update(sender,raw, instance,using,**kwargs):
            city = instance.city
            state = instance.state
            address = instance.address
            zipcode = instance.zipcode
            first_name = instance.first_name
            last_name = instance.last_name
            mobile_no = instance.mobile_no
            obj = Customer.objects.filter(user = instance, user_address =True).update(name = first_name+ " "+last_name, mobile_no = mobile_no,state=state, city=city, locality=address, zipcode=zipcode, user = instance)
            print("done1")
            

            
     
    




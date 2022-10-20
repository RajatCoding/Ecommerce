from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.utils.translation import gettext_lazy as _
from app.models import *




User = get_user_model()

# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', "first_name","last_name"]
    list_display_links = ['email', "last_name"]
    list_filter = ['email',"first_name"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info', {'fields': ("first_name", "last_name",  "mobile_no", "address", "city", "state", "zip_code")})),
        (('Permissions', {'fields': (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",)})),
         (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ("groups",
        "user_permissions",)
admin.site.register(User, UserAdmin)
admin.site.site_header = 'E-Commerce project'        
admin.site.index_title = 'E-Commerce Information'  


class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]



class CustomerAdmin(admin.ModelAdmin):
     list_display = ["user", "name", "mobile_no", "locality", "city", "state", "zipcode"]

class Product_Status_Admin(admin.ModelAdmin):
    list_display = ["user", "product", "customer", "quantity", 'ordered_date', "status" ]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "selling_price", "discounted_price", "category", "product_image"]


admin.site.register(Product,ProductAdmin)
admin.site.register(Product_Status,Product_Status_Admin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Cart,CartAdmin)

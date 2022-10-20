from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordResetDoneView
from .forms import LoginForm,PwdChange

urlpatterns = [

    #Home
    path('', views.home, name="home"),

#---------------------------------------------------------------------------

#Product releted url
    path('mobile/', views.mobile, name='mobile'),

    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),

    path('add-to-cart/<int:pk>', views.add_to_cart, name='add-to-cart'),
    path('showcart/', views.showcart, name='showcart'),

    path('buy/<int:pk>', views.buy_now, name='buy-now'),

    path('orders/', views.orders, name='orders'),
    
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.paymentdone, name='paymentdone'),

    path('pluscart/', views.plus),
    path('minuscart/', views.minus),
    path('removecart/', views.remove_cart),



#---------------------------------------------------------------------------

    #Address urls
    path('address/<int:pk>', views.add_address, name='address'),
    path('manageaddress/<int:pk>', views.manage_address, name= 'manageaddress'),
    path('addressupdate/<int:pk>', views.AddressUpdate.as_view(), name='addressupdate'),
    path('addressdelete/<int:pk>', views.AddressDelete.as_view(), name='addressdelete'),

   #---------------------------------------------------------------------------

#Change password Urls
    path('changepassword/', PasswordChangeView.as_view(template_name='app/changepassword.html', form_class =PwdChange,
    success_url= '/password_change_done/' ), name='changepassword'),

    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='app/changepassworddone.html' ), name='password_cahnge_done'),

    #--------------------------------------------------------------------------

#Reset password Urls Urls
    path('password_reset/', PasswordResetView.as_view(template_name='app/resetpassword.html' ), name='password_reset'),

    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='app/resetpasswordconfirm.html' ), name='password_reset_confirm'),

    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='app/resetpasswordcomplete.html' ), name='password_reset_complete'),

    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='app/resetpassworddone.html' ), name='password_reset_done'),

#------------------------------------------------------------------------------

#User Releted Authentication Urls
    path('registration/', views.customerregistration, name='customerregistration'),

    path('verify_otp/', views.verify_otp, name="otp"),

    path('login/', LoginView.as_view(template_name = 'app/login.html',authentication_form=LoginForm),name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('profile/<int:pk>', views.ProfileUpdate.as_view(), name='profile'),

#------------------------------------------------------------------------------
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

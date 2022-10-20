from . models import Cart
# from django.shortcuts import redirect
# def cart(request):
#       if request.user.is_authenticated:
#             cart_obj = Cart.objects.filter(user = request.user)
#             return(request, {'cat':cart_obj})
#       else:
#             return None

def cartt(request):
    cart_obj = None
    if request.user.is_authenticated:
        try:
            cart_obj = Cart.objects.filter(user = request.user)
        except :
            print("exception")
            pass
    if cart_obj:
        return( {'cat':cart_obj})
    else:  
      return {'cat':cart_obj }
# vip_section/urls.py   
from django.urls import path
from .views import vip_form,esewa_success,esewa_failure,khalti_payment,khalti_success,offline_payment

app_name = 'vip_section'  # Define the app namespace

urlpatterns = [
        path('vip_form/<int:subject_id>/',vip_form, name='vip_form'),
    
        path('esewa_success/', esewa_success, name='esewa_success'),
        path('esewa_failure/', esewa_failure, name='esewa_failure'),
        path('khalti_payment/', khalti_payment, name='khalti_payment'),
        path('khalti_success/', khalti_success, name='khalti_success'),
        path('offline_payment/', offline_payment, name='offline_payment'),
        



]


# # vip_section/urls.py   
# from django.urls import path
# from .views import esewa_payment_form, Pay_with_esewa_button

# app_name = 'vip_section'  # Define the app namespace

# urlpatterns = [
#         path('esewa_payment_form/', esewa_payment_form, name='esewa_payment_form'),
#         path('Pay_with_esewa_button/', Pay_with_esewa_button, name='Pay_with_esewa_button')


# ]
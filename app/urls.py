from django.urls import path
from . import views
from . import utils
urlpatterns =[
    path('verify-otp/',views.verify_otp),
   path('generate-otp/', views.send_otp, name='generate_otp'),
   path('add/',views.add_client),
   path('login/', views.login), 
    path('admin2/',views.admin2),
    path('logout/', views.logout) 
]
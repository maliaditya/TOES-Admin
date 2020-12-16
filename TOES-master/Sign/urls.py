from django.urls import path , include
from . import views

urlpatterns = [


    path('', views.sign_in ,name ='sign_in'),
    path('sign_up/' , views.sign_up , name = 'sign_up'),
    path('forget_pass/', views.forget_pass , name = 'forget_pass'),
    path('home/' , views.home , name = 'Home'),
    path('register/' , views.register , name = 'register'),
    path('create/' , views.create , name = 'create'),
    path('phone_disp/' , views.phone_disp , name = 'phone_disp'),
    path('workers/' ,views.workers , name ='workers' ),
    path('recruiters/' ,views.recruiters , name ='recruiters' ),
    
]

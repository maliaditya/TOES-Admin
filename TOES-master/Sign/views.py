from django.shortcuts import render,redirect
import datetime
from django.http import HttpResponse
# Create your views her

from requests.auth import HTTPBasicAuth
import requests
import json

AUTH_TOKEN = None

def sign_in(request):
    if request.method == 'POST':

        #Retriving username & password form login form template
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        data = {
            'password':  password,
            'phone': phone,
        }

        try:
        # post login details to this api
            url = 'http://52.201.220.252/token/login/'
            result = requests.post(url, json=data)
        except requests.RequestException:
            print('wrong login fields')
        #accessing token and putting it into djoser Authorization format
        global AUTH_TOKEN 
        AUTH_TOKEN = 'Token {}'.format(result.json()['auth_token'])
        print(AUTH_TOKEN)
        #This Api provides User Information name , is_admin, is_superuser, email, phone etc
        user_info_api = 'http://52.201.220.252/users/me/'

        #requsting user info form api
        user_info = requests.get(user_info_api, headers={'Authorization': AUTH_TOKEN})

        #storing userinfo response in access in json format
        access = user_info.json()

        #condition so that only admin and superuser can login
        if access['is_admin'] == True or access['is_superuser']==True:
            return redirect('Home')
        else:
            message="You Don’t Have Permission To Access on this Server"
            return HttpResponse(message)
    return render(request , 'Sign/sign_in.html')


def sign_up(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        data = {
            "counter": 0,
                "isVerified": 1,
                "is_superuser": 1,
                "is_admin": 1,
                "first_name": name,
                "last_name": "admin",
                "username": username,
                "password": password,
                "dob": "1998-06-02",
                "gender": 0,
                "aadhar_no": 0,
                "address": "pune",
                "smartphone": 1,
                "phone": phone,
                "re_password": re_password
        }
        
        create_user_api = 'http://52.201.220.252/users/'
        requests.post(create_user_api, json=data)
        return redirect('sign_in')
    return render(request , 'Sign/sign_up.html')


def forget_pass(request):
    return render( request , 'Sign/forget_pass.html')

# def home(request):
#     if request.method=='POST':
#         url = 'http://52.201.220.252/token/logout/'
#         result = requests.post(url, headers={'Authorization': AUTH_TOKEN})
#         print(result.json())
#         return redirect('sign_in')
#     return render(request, 'Sign/home.html')

def home(request):
    url = 'http://52.201.220.252/api/worker_count/'
    result = requests.get(url, headers={'Authorization': AUTH_TOKEN})
    data = result.json()
    print(data)
    print('This is required',data)
    if request.method=='POST':
        url = 'http://52.201.220.252/token/logout/'
        result = requests.post(url, headers={'Authorization': AUTH_TOKEN})
        print(result.json())
        return redirect('sign_in')
    return render(request, 'Sign/home.html',data)


def register(request):
    return render(request, 'Sign/register.html')

def create(request):
    return render( request , 'Sign/create.html')

def phone_disp(request):
    return render( request , 'Sign/phone_disp.html')

def recruiters(request):
    return render(request , 'Sign/recruiters.html')

def workers(request):
    return render(request , 'Sign/workers.html')

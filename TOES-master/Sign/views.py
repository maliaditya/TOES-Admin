from django.shortcuts import render,redirect
import datetime
from django.http import HttpResponse
# Create your views her
from django.contrib import messages
from requests.auth import HTTPBasicAuth
import requests
import json

AUTH_TOKEN = None
USER_ID = None
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
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            username = request.POST.get('username')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            aadhar = request.POST.get('adhar_no')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')
            
            data = {
                "counter": 0,
                    "isVerified": 0,
                    "is_superuser": 0,
                    "is_admin": 1,
                    "first_name": fname,
                    "last_name": lname,
                    "username": username,
                    "password": password,
                    "dob": dob,
                    "gender": gender,
                    "aadhar_no": aadhar,
                    "address":address,
                    "smartphone": 0,
                    "phone": phone,
                    "re_password": re_password
            }
            create_user_api = 'http://52.201.220.252/users/'
            response = requests.post(create_user_api, json=data)
            d = response.json()
            if response.status_code == 201:
                messages.success(request,"Account Created..!")
            else:
                for a,b in d.items():
                    messages.error(request,a+" "+b[0])
            
    return render(request , 'Sign/sign_up.html')


def forget_pass(request):
    return render( request , 'Sign/forget_pass.html')

def home(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/worker_count/'
        result = requests.get(url, headers={'Authorization': AUTH_TOKEN})
        data = result.json()
        if request.method=='POST':
            url = 'http://52.201.220.252/token/logout/'
            result = requests.post(url, headers={'Authorization': AUTH_TOKEN})
            return redirect('sign_in')
        return render(request, 'Sign/home.html',data)


def register(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        return render(request, 'Sign/register.html')

def create(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        if request.method == 'POST':
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                username = request.POST.get('username')
                dob = request.POST.get('dob')
                gender = request.POST.get('gender')
                aadhar = request.POST.get('adhar_no')
                address = request.POST.get('address')
                phone = request.POST.get('phone')
                password = request.POST.get('password')
                re_password = request.POST.get('re_password')
                category1 = request.POST.get('category1')
                category1vc = request.POST.get('category1vc')
                category1exp = request.POST.get('category1exp')
                category2 = request.POST.get('category2')
                category2vc = request.POST.get('category2vc')
                category2exp = request.POST.get('category2exp')
                category3 = request.POST.get('category3')
                category3vc = request.POST.get('category3vc')
                category3exp = request.POST.get('category3exp')
                
                data = {
                    "counter": 0,
                        "isVerified": 0,
                        "is_superuser": 0,
                        "is_admin": 0,
                        "first_name": fname,
                        "last_name": lname,
                        "username": username,
                        "password": password,
                        "dob": dob,
                        "gender": gender,
                        "aadhar_no": aadhar,
                        "address":address,
                        "smartphone": 0,
                        "phone": phone,
                        "re_password": re_password
                }
                create_user_api = 'http://52.201.220.252/users/'
                response = requests.post(create_user_api, json=data)
                d = response.json()
                if response.status_code == 201:
                    messages.success(request,"Account Created..!")
                else:
                    for a,b in d.items():
                        messages.error(request,a+" "+b[0])
                data = {

                    "city": "Pune",
                    "category_1": category1,
                    "category_1_vc": category1vc,
                    "category_1_exp": category1exp,
                    "category_2": category2,
                    "category_2_vc": category2vc,
                    "category_2_exp": category2exp,
                    "category_3": category3,
                    "category_3_vc": category3vc,
                    "category_3_exp": category3exp,
                    "user": d['id']
                
                }

                url = 'http://52.201.220.252/worker/'
                response = requests.post(url, json=data ,headers={'Authorization': AUTH_TOKEN})
                d = response.json()
                if response.status_code == 201:
                    messages.success(request,"details entered successful")
                else:
                    for a,b in d.items():
                        messages.error(request,a+" "+b[0])
        return render( request , 'Sign/create.html')

def phone_disp_second(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        return render( request , 'Sign/phone_disp_second.html' )

def phone_disp(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/withoutsmartphone/'
        response = requests.get(url , headers = {'Authorization' : AUTH_TOKEN})
        response = response.json()

    return render( request , 'Sign/phone_disp.html',{'response'  :response} )

def recruiters(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/job/'
        response = requests.get(url , headers = {'Authorization' : AUTH_TOKEN})
        response = response.json()
        return render(request , 'Sign/recruiters.html', {'response' : response})

def workers(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/allcategories/'
        json_data={}
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        response=response.json()
        return render(request,'Sign/workers.html', {'response' : response})

def workerpainter(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/category/painter/'
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        response=response.json()
        return render(request , 'Sign/workerpainter.html',{'response':response})


def workerplumber(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/category/plumber/'
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        response=response.json()
        return render(request , 'Sign/workerplumber.html',{'response':response})



# def profile(request):
    
#     url = 'http://52.201.220.252/users/me/'
#     response = requests.get(url , headers={'Authorization':AUTH_TOKEN})
#     response=response.json()
#     return render(request , 'Sign/profile.html',{'response':response})

def driver(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/category/driver/'
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        response=response.json()
        return render(request , 'Sign/driver.html',{'response':response})



def electrician(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/category/electrician/'
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        response=response.json()
        return render(request , 'Sign/electrician.html',{'response':response})



def carpenter(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/api/category/carpenter/'
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        response=response.json()
        return render(request , 'Sign/carpenter.html',{'response':response})


def profile(request):
    if AUTH_TOKEN == None:
        return redirect('sign_in')
    else:
        url = 'http://52.201.220.252/users/me/'
        response = requests.get(url , headers={'Authorization': AUTH_TOKEN})
        data = response.json()
        name = data["first_name"] + " " +data['last_name']
        mobile = data['phone']
        address = data['address']
        dob = data['dob']
        gender=data['gender']
        username=data['username']

        return render(request , 'Sign/profile.html',{'name':name,'mobile':mobile,'address':address,'dob':dob,'gender':gender,'username':username})

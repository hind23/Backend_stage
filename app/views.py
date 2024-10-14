from django.shortcuts import render
from datetime import datetime
import pyotp
from django.shortcuts import render
from datetime import datetime
import pyotp


from django.core.mail import send_mail
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
from . import models
import jwt
from .models import Admin
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

SECRET_KEY = settings.SECRET_KEY

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipient_email = data.get('email')    
        totp = pyotp.TOTP(pyotp.random_base32(), interval=600)
        otp = totp.now()
        valid_date = datetime.now() + timedelta(minutes=10)
        token = jwt.encode({
            'otp_generated': True,
            'otp_secret': totp.secret,
            'otp_valid_date': valid_date.isoformat()
        }, SECRET_KEY, algorithm='HS256')

        # Send OTP to user's email
        subject = 'Your OTP Code'
        message = f'Here is your OTP code: {otp}\nThis code is valid for the next 10 minutes.'
        from_email = settings.EMAIL_HOST_USER  # Make sure this is configured in your settings
        recipient_list = [recipient_email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list)

        # Send the token back to the client
        return JsonResponse({'message': 'OTP generated and sent to your email!', 'token': token})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def home(request):
    return render(request, 'home.html')



@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            otp = data.get('otp')
            token = data.get('token')  
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            otp_secret = decoded_token['otp_secret']
            otp_valid_date = decoded_token['otp_valid_date']
            valid_until = datetime.fromisoformat(otp_valid_date)
            if datetime.now() > valid_until:
                print('expired')
                return JsonResponse({'error': 'OTP has expired'}, status=400)

            # Verify OTP
            totp = pyotp.TOTP(otp_secret, interval=600)
            if totp.verify(otp):
                print("success !!!")
                return JsonResponse({'message': 'OTP verified successfully!'}, status=200)
            else:
                print('not seccued !!!')
                return JsonResponse({'error': 'Invalid OTP'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'OTP has expired'}, status=400)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def add_client(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data is None :
                return JsonResponse({'error': 'Invalid data'}, status=400)
            nom = data.get('nom')
            prenom = data.get('prenom')
            email = data.get('email')
            phone = data.get('phone')
            revenu = data.get('revenu')
            age = data.get('age')
            revenue_codebiteur = data.get('revenue_codebiteur', None)
            age_codebiteur = data.get('age_codebiteur', None)
            type_credit = data.get('type_credit')
            frequence = data.get('frequence')
            duree = data.get('duree')
            hamish_jiddiya = data.get('hamish_jiddiya', None)
            credit = data.get('credit')
            client =models.Client( nom=nom,
                prenom=prenom,
                email=email,
                phone=phone,
                revenu=revenu,
                age=age,
                revenue_codebiteur=revenue_codebiteur,
                age_codebiteur=age_codebiteur,
                type_credit=type_credit,
                frequence=frequence,
                duree=duree,
                hamish_jiddiya=hamish_jiddiya,
                credit=credit)
            client.save()
            return JsonResponse({'message': 'Data added successfully!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login(request):
    print('yayyyyy')
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        
        admin = Admin.objects.filter(email=email).first()       
        if admin is None:
            raise AuthenticationFailed('User not found!')      
        if admin.password != password:
            raise AuthenticationFailed('Incorrect password')
        print('conncetec')
        payload = {
            'id': admin.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print('JWT Cookie set: %s' % token)  # Log le cookie JWT dans la console
        if isinstance(token, bytes):
            token = token.decode('utf-8')  # Convert bytes to string

        response = JsonResponse({
            'jwt': token
        })
        response.set_cookie(key='jwt', value=token, httponly=True, secure=True, samesite='None')      
        return response
    return JsonResponse({'error': 'Invalid method'}, status=405)

def admin2(request):
    print('User view called')  # Vérifiez si cette ligne est imprimée
    print(request.COOKIES)
    token = request.COOKIES.get('jwt')
    print('here is the token: %s' % token)
    if not token:
        raise AuthenticationFailed('Aukkthentication token not provided')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated: Token has expired')

    admin = Admin.objects.get(id=payload['id'])
    admin_data = {
        'nom': admin.nom,
        'prenom': admin.prenom
    }
    
    return JsonResponse(admin_data)

def logout(request):
    if request.method == 'POST':
        # Log the cookies that were sent with the request
        print('Request Cookies:', request.COOKIES)
        
        # Create a response to send back to the client
        response = JsonResponse({'message': 'Successfully logged out!'})
        
        # Delete the 'jwt' cookie
        response.delete_cookie('jwt', path='/',samesite='None')  
        print('Deleting jwt cookie...') 
        # Check if the cookie was indeed deleted in the response
        # (Note: request.COOKIES won't change here)
        print('Cookies after delete_cookie call:', request.COOKIES)
        
        return response
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .import models
from .import serializers
from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
#email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.contrib import messages

User= get_user_model()

# Create your views here.
class All_Users(ModelViewSet):
    queryset= User.objects.all()
    serializer_class= serializers.UserSerializer
    
    
class RegistrationView(APIView):
    serializer_class= serializers.RegistrationSerializer
    def post(self, request):
        next= request.GET.get('next')
        serializer= serializers.RegistrationSerializer(data=request.data)
        print('Reached this function')
        
        if serializer.is_valid():
            print('valid')
            new_user= serializer.save()
            password= serializer.validated_data.get('password')
            new_user.set_password(password)
            new_user.save()
            print('User saved')
            
        #sending email
            if new_user.email_is_verified == False:
                
                current_site= get_current_site(request)
                user= new_user
                uid= urlsafe_base64_encode(force_bytes(user.pk))
                token= account_activation_token.make_token(user)
                print(uid, token)
                email= user.email
                subject= "Verify Your Email Address"
                message = render_to_string('verifyEmail.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
                
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            print('Email should be sent')
            return Response('Please Check Your Email')
                
        else:  
            print(serializer.errors)
        return Response(serializer.errors)
    
def activate(request, uidbd64, token):
    next= request.GET.get('next')
    print(uidbd64, token)
    
    try:
        uid= force_str(urlsafe_base64_decode(uidbd64))
        user= User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified=True 
        user.save()
        # messages.success(request,'Your account has been verified successfully')
        return Response('Your account has been verified successfully. You may proceed to log in.')
    
    return redirect('register')


class LoginView(APIView):
    serializer_class= serializers.LoginSerializer
    
    def post(self, request):
        email= request.data.get('email')
        password= request.data.get('password')
        
        user= authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response('Login Successful')
        
        return redirect('register')
    
class LogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
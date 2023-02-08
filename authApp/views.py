from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from allauth.account.models import EmailAddress 
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from dj_rest_auth.registration.serializers import  ResendEmailVerificationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
#from dj_rest_auth.app_settings import PasswordResetSerializer
from .serializers import MyCustomPasswordResetSerializer
from django.contrib.auth import get_user_model
from allauth.account.views import ConfirmEmailView,PasswordResetView

from .forms import MyCustomResetPasswordForm
    
# Create your views here.

    
    
class Mod_ResendEmailVerificationView(CreateAPIView):       #this was originally a class from dj_rest_auth.registration.views, 
    permission_classes = (AllowAny,)                        #it was modified to give adequate Response detail to the FE,
    serializer_class = ResendEmailVerificationSerializer    #instaed of "ok" all d time 
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        if email and not email.verified:
            email.send_confirmation(request)
        elif not email:
            return Response({'detail': _('No Account was found with this email')}, status=status.HTTP_404_NOT_FOUND)
        elif email.verified:
            return Response({'detail': _('Email has been verified already')}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)
    


"""
This was originally a class from dj_rest_auth.views,
it was modified to give adequate Response detail to the FE,
instaed of "ok" all d time.

"""
class Mod_PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    
    serializer_class = MyCustomPasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'
    queryset = EmailAddress.objects.all()
    
    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        serializer.save()
        if email and email.verified:
            return Response({'detail': _('Password reset e-mail has been sent.')},status=status.HTTP_200_OK,)
        elif not email:
            return Response({'detail': _('No Account was found with this email')}, status=status.HTTP_404_NOT_FOUND)
        elif not email.verified:
            return Response({'detail': _('Email has not been verified.')}, status=status.HTTP_400_BAD_REQUEST)

        
class CustomPasswordResetView(PasswordResetView):
    form_class = MyCustomResetPasswordForm


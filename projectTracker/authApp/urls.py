from django.urls import path, include,re_path
from dj_rest_auth.registration.views import  RegisterView, VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from django.views.generic import TemplateView
from allauth.account.views import email_verification_sent 
from .views import Mod_ResendEmailVerificationView, Mod_PasswordResetView, CustomPasswordResetView

from .socialviews import GoogleLogin

urlpatterns = [
    path('/password/reset/', Mod_PasswordResetView.as_view(), name='rest_password_reset'),
    path('/', include('dj_rest_auth.urls')),
    path('/registration/', RegisterView.as_view(),name='rest_register'),
    path('/registration/account-confirm-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    re_path(r'^/registration/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),name='account_confirm_email'),
    path("/registration/account-confirm-email/",email_verification_sent,name="account_email_verification_sent"),
    path('/registration/resend-email/', Mod_ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    #social login
    path('/google/', GoogleLogin.as_view(), name='google_login')
    
]


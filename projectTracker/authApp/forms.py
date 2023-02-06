from __future__ import absolute_import
#some comment
from django.conf import settings
from allauth.account.forms import ResetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from allauth.utils import (
    build_absolute_uri,
)
from allauth.account.forms import default_token_generator
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.app_settings import AuthenticationMethod
from allauth.account.models import EmailAddress
from allauth.account.utils import (
    user_pk_to_url_str,
    user_username,
)

from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.utils import (user_pk_to_url_str, user_username)
from allauth.utils import build_absolute_uri

class MyCustomResetPasswordForm(ResetPasswordForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a string containing the email address supplied
        email_address = super(MyCustomResetPasswordForm, self).save(request)
        # Add your own processing here.
        # Ensure you return the original result
        return email_address
        
    def _send_password_reset_mail(self, request, email, users, **kwargs):
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in users:
            temp_key = token_generator.make_token(user)
            uid=user_pk_to_url_str(user)
            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()
            # send the password reset email
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            url = build_absolute_uri(request, path)
            context = {
                "request": request,
                "current_site": get_current_site(request),
                "user": user,
                "password_reset_url": url,
                "key": temp_key,
                "uid": uid
            }
            if app_settings.AUTHENTICATION_METHOD != AuthenticationMethod.EMAIL:
                context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
            
            
            
class MyCustomAllAuthPasswordResetForm(MyCustomResetPasswordForm):


    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)
            uid = user_pk_to_url_str(user)
            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse(
                'password_reset_confirm',
                args=[user_pk_to_url_str(user), temp_key],
            )

            if getattr(settings, 'REST_AUTH_PW_RESET_USE_SITES_DOMAIN', False) is True:
                url = build_absolute_uri(None, path)
            else:
                url = build_absolute_uri(request, path)

            context = {
                'request': request,
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'key': temp_key,
                "uid": uid
            }
            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']
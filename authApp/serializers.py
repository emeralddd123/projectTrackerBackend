from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from .forms import MyCustomAllAuthPasswordResetForm
from django.contrib.auth.forms import PasswordResetForm


class MyCustomPasswordResetSerializer(PasswordResetSerializer):
    
    @property
    def password_reset_form_class(self):
        if 'allauth' in settings.INSTALLED_APPS:
            return MyCustomAllAuthPasswordResetForm
        else:
            return PasswordResetForm
        
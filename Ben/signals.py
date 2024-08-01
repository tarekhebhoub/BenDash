# signals.py
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from rest_framework.authtoken.models import Token

@receiver(user_logged_in)
def create_auth_token(sender, request, user, **kwargs):
    """
    A signal receiver which creates a new token upon user login.
    """
    Token.objects.get_or_create(user=user)

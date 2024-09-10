from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        try:
            # Fetch user by email (case insensitive)
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None

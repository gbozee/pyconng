from django.contrib.auth.backends import ModelBackend
from django.db import models
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = UserModel.objects.filter(
            models.Q(username=username) | models.Q(email=username)).first()
        if user:
            if user.check_password(password):
                return user
        return None

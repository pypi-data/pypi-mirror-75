from django.contrib.auth import backends

from django.contrib.auth import get_user_model


User = get_user_model()


class EmailAuthBackend(backends.ModelBackend):
    """
    Email Authentication Backend

    Allows a user use the email as username to authenticate.
    If authentication fails, make another try with the username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """E-mail and password authentication."""
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """Get a `User` from its `user_id`."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

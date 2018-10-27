from accounts.models import MyCustomUser

class CustomUserAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = MyCustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except MyCustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = MyCustomUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except MyCustomUser.DoesNotExist:
            return None
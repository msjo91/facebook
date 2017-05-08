from django.contrib.auth import get_user_model

User = get_user_model()


class FacebookBackend():
    def authenticate(self, facebook_id, **extra_fields):
        user, user_created = User.objects.get_or_create(username=facebook_id)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

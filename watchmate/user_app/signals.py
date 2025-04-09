from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def generate_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         print('COMING HERE')
#         Token.objects.create(user=instance)
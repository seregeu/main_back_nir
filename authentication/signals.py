import django.dispatch
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import UserProfile

token_obtained = django.dispatch.Signal()


class JSONWebToken:
    def obtained(self, user):
        token_obtained.send(sender=self.__class__, user=user)


@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

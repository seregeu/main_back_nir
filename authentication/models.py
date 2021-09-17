from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, default="")
    cards = models.CharField(max_length=16, default="")
    second_mail = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=15, default="")

    def __str__(self):
        return f"Username: {self.user.username} "\
                f"gender: {self.gender} "\
                f"cards: {self.cards} "\
                f"second_mail: {self.second_mail} "\
                f"phone: {self.phone}"

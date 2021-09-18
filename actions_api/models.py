from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

ACTION_CHOICES = (
    (1, 'Comment'),
    (2, 'Download'),
    (3, 'Rating'),
    (4, 'Run'),
    (5, 'Stop')
)


class Action(models.Model):
    user = models.ForeignKey(User, related_name='user_actions', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    app_id = models.IntegerField()
    data = models.CharField(max_length=200)
    action_type = models.IntegerField(choices=ACTION_CHOICES)

    def __str__(self):
        return f"app_id: {self.app_id} " \
               f"user: {self.user.username} " \
               f"date: {self.date} " \
               f"action_type: {self.action_type} "\
               f"data: {self.data} " \



from django.db import models
from authentication.models import UserProfile


class AppApi(models.Model):
    title = models.CharField(max_length=20)
    rating = models.IntegerField()
    image_url = models.CharField(max_length=100)
    downloads_amount = models.IntegerField()
    app_id = models.IntegerField(default=0)

    def __str__(self):
        return f"app_id: {self.app_id} " \
               f"title: {self.title} " \
               f"rating: {self.rating} " \
               f"image_url: {self.image_url} " \
               f"download amount: {self.downloads_amount}"


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    app = models.ForeignKey(AppApi, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, default="")

    def __str__(self):
        return f"content: {self.content}"


class Download(models.Model):
    user = models.OneToOneField(UserProfile, related_name='downloads', on_delete=models.CASCADE)
    apps = models.ManyToManyField(AppApi, related_name='downloads')

    def __str__(self):
        return f"user: {self.user.user.username}"

from rest_framework import serializers

class AppApiSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    rating = serializers.IntegerField()
    image_url = serializers.CharField(max_length=100)
    downloads_amount = serializers.IntegerField()

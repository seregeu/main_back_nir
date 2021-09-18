from rest_framework import serializers

class ActionAPISerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    data = serializers.CharField(max_length=200, default="")
    action_type = serializers.ChoiceField(choices=[1, 2, 3, 4, 5], required=True)

from rest_framework.serializers import ModelSerializer

from .models import Post, Subscription


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
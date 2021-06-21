from rest_framework.decorators import action
from priorityapi.models import PriorityUser, Subscription
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from rest_framework import status
from django.utils import timezone

class SubscriptionViewSet(ViewSet):
    def create(self, request):
        if request.data['subscribed']:
            subscription = Subscription()
            subscription.creator_id = request.data['creator_id']
            subscription.subscriber = PriorityUser.objects.get(user=request.auth.user)
            subscription.save()
            serializer = SubscriptionSerializer(subscription, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            requesting_priority_user = PriorityUser.objects.get(user=request.auth.user)
            subscription = Subscription.objects.get(creator_id=request.data['creator_id'], subscriber=requesting_priority_user)
            subscription.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class PriorityUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = PriorityUser
        fields = ('user',)

class SubscriptionSerializer(serializers.ModelSerializer):
    creator = PriorityUserSerializer(many=False)
    subscriber = PriorityUserSerializer(many=False)
    class Meta:
        model = Subscription
        fields = ('id', 'creator', 'subscriber', 'created_on')

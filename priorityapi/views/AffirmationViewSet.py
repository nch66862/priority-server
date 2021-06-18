from django.http.response import HttpResponse
from rest_framework.decorators import action
from priorityapi.models import PriorityUser, Subscription, History, What, Priority, Affirmation, affirmation
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from rest_framework import status
from django.utils import timezone
import json

class AffirmationViewSet(ViewSet):
    def list(self, request, pk):
        affirmations = Affirmation.objects.filter(priority_id=pk)
        affirmations_serialized = AffirmationSerializer(affirmations, many=True, context={'request': request})
        return Response(affirmations_serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        affirmation = Affirmation()
        affirmation.priority_user = PriorityUser.objects.get(user=request.auth.user)
        affirmation.priority = request.data['priority_id']
        affirmation.affirmation = request.data['affirmation']
        affirmation.save()
        serializer = AffirmationSerializer(affirmation, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        affirmation = Affirmation.objects.get(pk=pk)
        affirmation.delete()
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

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id', 'priority_user', 'priority', 'why', 'how', 'is_public', 'creation_date')

class AffirmationSerializer(serializers.ModelSerializer):
    priority_user = PriorityUserSerializer(many=False)
    priority = PrioritySerializer(many=False)
    class Meta:
        model = Priority
        fields = ('id', 'priority_user', 'priority', 'affirmation', 'created_on')

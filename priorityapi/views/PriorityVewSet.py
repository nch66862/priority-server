from django.http.response import HttpResponse
from rest_framework.decorators import action
from priorityapi.models import PriorityUser, Subscription, History, What, Priority
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from rest_framework import status
from django.utils import timezone
import json

class PriorityViewSet(ViewSet):
    def update(self, request, pk):
        priority = Priority.objects.get(pk=pk)
        priority.how=request.data['how']
        priority.priority=request.data['priority']
        priority.why=request.data['why']
        priority.save()
        serializer = PrioritySerializer(priority, context={'request': request})
        return Response(serializer.data)

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id', 'priority_user', 'priority', 'why', 'how', 'is_public', 'creation_date')
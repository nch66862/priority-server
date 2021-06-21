"""View module for handling requests about products"""
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from priorityapi.models import History
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

class HistoryViewSet(ViewSet):
    """Request handlers for Products in the Bangazon Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
        creates a new history record in the database
        """
        new_history = History()
        new_history.what_id = request.data["what_id"]
        new_history.goal_date = request.data["goal_date"]
        new_history.time_spent = request.data["time_spent"]
        new_history.save()
        serializer = HistorySerializer(new_history, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def list(self, request):
        """
        builds statistics for the history of the logged in user
        """
        serializer = HistorySerializer(new_history, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, pk):
        """
        builds statistics for the history of a priority_user with the provided pk
        """
        serializer = HistorySerializer(new_history, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('id', 'what', 'submission_date', 'goal_date', 'time_spent')
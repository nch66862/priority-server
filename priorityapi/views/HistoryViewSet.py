"""View module for handling requests about products"""
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from priorityapi.models import History, PriorityUser, What
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import datetime, timedelta
from django.db.models import Sum

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
        response = {}
        todays_date = datetime.date(datetime.today())
        comparison_date = todays_date
        last_date = None
        current_streak = 0
        current_user = PriorityUser.objects.get(user=request.auth.user)
        histories = History.objects.filter(what__priority__priority_user=current_user).order_by('-goal_date')
        for history in histories:
            if history.goal_date == last_date:
                None
            elif history.goal_date == comparison_date:
                current_streak += 1
                comparison_date = comparison_date - timedelta(days=1)
                last_date = history.goal_date
            else:
                break
        seven_day_time_spent = History.objects.filter(what__priority__priority_user=current_user, goal_date__range=[todays_date-timedelta(days=7), todays_date]).aggregate(week_total=Sum('time_spent'))
        week_total = WeekTotalSerializer(seven_day_time_spent, many=False, context={'request': request})
        total_time_query = History.objects.filter(what__priority__priority_user=current_user).aggregate(total_time=Sum('time_spent'))
        total_time_dict = TotalTimeSerializer(total_time_query, many=False, context={'request': request})

        response['current_streak'] = current_streak
        response['week_total'] = week_total.data['week_total']
        response['total_time'] = total_time_dict.data['total_time']
        return Response(response, status=status.HTTP_200_OK)

        # serializer = HistorySerializer(new_history, context={'request': request})
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, pk):
        """
        builds statistics for the history of a priority_user with the provided pk
        """
        # streak of days
        # total time this week
        # total time

        serializer = HistorySerializer(new_history, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = What
        fields = ('id', 'priority', 'what', 'is_deleted')

class HistorySerializer(serializers.ModelSerializer):
    what = WhatSerializer
    class Meta:
        model = History
        fields = ('id', 'what', 'submission_date', 'goal_date', 'time_spent')

class WeekTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('week_total',)

class TotalTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('total_time',)
"""View module for handling requests about products"""
from priorityapi.models.priority import Priority
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
        serializer = HistorySerializer(
            new_history, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        builds statistics for the history of the logged in user
        """
        # establish custom variable to send back
        response = {}

        # Find a streak by adding a number to current streak. Start at today. Work backwards until no more histories or a date is skipped.
        todays_date = datetime.date(datetime.today())
        comparison_date = todays_date
        last_date = None
        current_streak = 0
        current_user = PriorityUser.objects.get(user=request.auth.user)
        # Sort by the date - newest first
        histories = History.objects.filter(
            what__priority__priority_user=current_user).order_by('-goal_date')
        for history in histories:
            # Have to have this initial check for multiple entries in the same day
            if history.goal_date == last_date:
                None
            # Counts up and sets the next date when the streak continues
            elif history.goal_date == comparison_date:
                current_streak += 1
                comparison_date = comparison_date - timedelta(days=1)
                last_date = history.goal_date
            # Breaks out of the loop if the streak ends
            else:
                break
        # Add the streak to the response
        response['current_streak'] = current_streak

        # Filter the history for the current user data only. limit to data only in the past week. total up the time for this data.
        seven_day_time_spent = History.objects.filter(what__priority__priority_user=current_user, goal_date__range=[
                                                      todays_date-timedelta(days=6), todays_date]).aggregate(week_total=Sum('time_spent'))
        week_total_dict = WeekTotalSerializer(
            seven_day_time_spent, many=False, context={'request': request}).data
        response['week_total'] = week_total_dict['week_total']

        # Filter the history for the current user data only. limit to data only in the past week. total up the time for this data.
        total_time_query = History.objects.filter(
            what__priority__priority_user=current_user).aggregate(total_time=Sum('time_spent'))
        total_time_dict = TotalTimeSerializer(
            total_time_query, many=False, context={'request': request}).data
        response['total_time'] = total_time_dict['total_time']

        # Set up the data structure that chart.js needs
        response['line_chart'] = {
            'data': {
                'labels': [],
                'datasets': [{
                    'label': 'time',
                    'data': [],
                    'color': ['black'],
                    'borderColor': ['black'],
                    'borderWidth': 1
                }]
            }
        }
        # put all of the dates in for the labels along the x-axis of the line chart
        for day_offset in range(7):
            response['line_chart']['data']['labels'].append(
                todays_date - timedelta(days=day_offset))
        # query to get the time every day and add that y value for each x value
        for day in response['line_chart']['data']['labels']:
            time_today_query = History.objects.filter(
                what__priority__priority_user=current_user, goal_date=day).aggregate(time_today=Sum('time_spent'))
            time_today_dict = TimeTodaySerializer(
                time_today_query, many=False, context={'request': request}).data
            if time_today_dict['time_today'] is not None:
                response['line_chart']['data']['datasets'][0]['data'].append(
                    time_today_dict['time_today'])
            else:
                response['line_chart']['data']['datasets'][0]['data'].append(0)

        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        builds statistics for the history of a priority_user with the provided pk
        """
        # establish custom variable to send back
        response = {}

        # Find a streak by adding a number to current streak. Start at today. Work backwards until no more histories or a date is skipped.
        todays_date = datetime.date(datetime.today())
        comparison_date = todays_date
        last_date = None
        current_streak = 0
        current_user_priority = Priority.objects.get(pk=pk)
        current_user = PriorityUser.objects.get(pk=current_user_priority.priority_user_id)
        # Sort by the date - newest first
        histories = History.objects.filter(
            what__priority__priority_user=current_user).order_by('-goal_date')
        for history in histories:
            # Have to have this initial check for multiple entries in the same day
            if history.goal_date == last_date:
                None
            # Counts up and sets the next date when the streak continues
            elif history.goal_date == comparison_date:
                current_streak += 1
                comparison_date = comparison_date - timedelta(days=1)
                last_date = history.goal_date
            # Breaks out of the loop if the streak ends
            else:
                break
        # Add the streak to the response
        response['current_streak'] = current_streak

        # Filter the history for the current user data only. limit to data only in the past week. total up the time for this data.
        seven_day_time_spent = History.objects.filter(what__priority__priority_user=current_user, goal_date__range=[
                                                      todays_date-timedelta(days=6), todays_date]).aggregate(week_total=Sum('time_spent'))
        week_total_dict = WeekTotalSerializer(
            seven_day_time_spent, many=False, context={'request': request}).data
        response['week_total'] = week_total_dict['week_total']

        # Filter the history for the current user data only. limit to data only in the past week. total up the time for this data.
        total_time_query = History.objects.filter(
            what__priority__priority_user=current_user).aggregate(total_time=Sum('time_spent'))
        total_time_dict = TotalTimeSerializer(
            total_time_query, many=False, context={'request': request}).data
        response['total_time'] = total_time_dict['total_time']

        # Set up the data structure that chart.js needs
        response['line_chart'] = {
            'data': {
                'labels': [],
                'datasets': [{
                    'label': 'time',
                    'data': [],
                    'color': ['black'],
                    'borderColor': ['black'],
                    'borderWidth': 1
                }]
            }
        }
        # put all of the dates in for the labels along the x-axis of the line chart
        for day_offset in range(7):
            response['line_chart']['data']['labels'].append(
                todays_date - timedelta(days=day_offset))
        # query to get the time every day and add that y value for each x value
        for day in response['line_chart']['data']['labels']:
            time_today_query = History.objects.filter(
                what__priority__priority_user=current_user, goal_date=day).aggregate(time_today=Sum('time_spent'))
            time_today_dict = TimeTodaySerializer(
                time_today_query, many=False, context={'request': request}).data
            if time_today_dict['time_today'] is not None:
                response['line_chart']['data']['datasets'][0]['data'].append(
                    time_today_dict['time_today'])
            else:
                response['line_chart']['data']['datasets'][0]['data'].append(0)

        return Response(response, status=status.HTTP_200_OK)


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


class TimeTodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('time_today',)

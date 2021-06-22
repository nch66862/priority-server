from rest_framework.decorators import action
from priorityapi.models import PriorityUser, Subscription, History, What, Priority
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework import status

class PriorityUserViewSet(ViewSet):
    def retrieve(self, request, pk):
        try:
            priority = Priority.objects.get(pk=pk)
            priority_serialized = PrioritySerializer(priority, context={'request': request})
            user = PriorityUser.objects.get(pk=priority.priority_user_id)
            user_serialized = PriorityUserSerializer(user, context={'request': request})
            histories = History.objects.filter(what__priority_id=priority.id)
            history_serialized = HistorySerializer(histories, many=True, context={'request': request})
            response = {}
            response['user'] = user_serialized.data
            response['priority'] = priority_serialized.data
            response['history'] = history_serialized.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def list(self, request):
        priority_user = PriorityUser.objects.get(user=request.auth.user)
        priorities = Priority.objects.filter(is_public=True).exclude(priority_user__user=request.auth.user)

        # for every priority, see if the creator id on the subscription table matches the priority user id on the priority, then see if the user is in the subscription result
        for priority in priorities:
            matching_subscriptions = Subscription.objects.filter(creator_id=priority.priority_user_id)
            for subscription in matching_subscriptions:
                if priority_user.id == subscription.subscriber_id:
                    priority.priority_user.subscribed = True
                else:
                    priority.priority_user.subscribed = False

        community_serialized = CommunityListSerializer(priorities, many=True, context={'request': request})

        return Response(community_serialized.data)

    @action(methods=["GET"], detail=False)
    def my_profile(self, request):
        user = PriorityUser.objects.get(user=request.auth.user)
        user_serialized = PriorityUserSerializer(user, context={'request': request})
        priority = Priority.objects.get(priority_user_id=user.id)
        priority_serialized = PrioritySerializer(priority, context={'request': request})
        histories = History.objects.filter(what__priority__priority_user=user)
        history_serialized = HistorySerializer(histories, many=True, context={'request': request})
        response = {}
        response['user'] = user_serialized.data
        response['priority'] = priority_serialized.data
        response['history'] = history_serialized.data
        return Response(response, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=False)
    def change_privacy(self, request):
        priority = Priority.objects.get(priority_user__user=request.auth.user)
        if request.data['is_public'] == "true":
            priority.is_public = True
        else:
            priority.is_public = False
        priority.save()

        priority_serialized = PrioritySerializer(priority, context={'request': request})
        return Response(priority_serialized.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def subscriptions(self, request):
        priority_user = PriorityUser.objects.get(user=request.auth.user)
        subscriptions = Subscription.objects.filter(subscriber=priority_user)
        priorities = Priority.objects.filter(is_public=True).exclude(priority_user__user=request.auth.user)

        def subscription_filter(priority):
            for subscription in subscriptions:
                if subscription.creator_id == priority.priority_user_id:
                    return True
            return False
        priorities = filter(subscription_filter, priorities)
        
        subscriptions_serialized = SubscriptionListSerializer(priorities, many=True, context={'request': request})

        return Response(subscriptions_serialized.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class PriorityUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = PriorityUser
        fields = ('id', 'user', 'subscribed')

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id', 'priority_user', 'priority', 'why', 'how', 'is_public', 'creation_date')

class WhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = What
        fields = ('id', 'priority', 'what', 'is_deleted')

class HistorySerializer(serializers.ModelSerializer):
    what = WhatSerializer(many=False)
    class Meta:
        model = History
        fields = ('id', 'what', 'submission_date', 'goal_date', 'time_spent')

class CommunityListSerializer(serializers.ModelSerializer):
    priority_user = PriorityUserSerializer(many=False)
    class Meta:
        model = Priority
        fields = ('id', 'priority_user', 'priority', 'why', 'how', 'is_public', 'creation_date')

class SubscriptionListSerializer(serializers.ModelSerializer):
    priority_user = PriorityUserSerializer(many=False)
    class Meta:
        model = Priority
        fields = ('id', 'priority_user', 'priority', 'why', 'how', 'is_public', 'creation_date')

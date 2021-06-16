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

class PriorityUserViewSet(ViewSet):
    def retrieve(self, request, pk):
        try:
            user = PriorityUser.objects.get(pk=pk)
            subscribers = Subscription.objects.filter(author=pk, ended_on=None).count()
            user.subscribers = subscribers
            serializer = PriorityUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    #only returns list of active users
    def list(self, request):
        users = PriorityUser.objects.order_by('user__first_name').exclude(user=request.user).exclude(user__is_active=False)
        serializer = PriorityUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    def update(self, request, pk):
        if not request.auth.user.has_perm('rareapi.change_rareuser'):
            raise PermissionDenied()
        rareuser = PriorityUser.objects.get(pk=pk)
        rareuser.user.first_name = request.data["firstName"]
        rareuser.user.last_name = request.data["lastName"]
        rareuser.user.username = request.data["username"]
        rareuser.bio = request.data["bio"]
        rareuser.user.email = request.data["email"]
        rareuser.user.save()
        rareuser.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        if not request.auth.user.has_perm('rareapi.delete_rareuser'):
            raise PermissionDenied()
        try:
            rareuser = PriorityUser.objects.get(pk=pk)
            rareuser.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)
    @action(detail=False)
    def inactive(self, request):
        if not request.auth.user.has_perm('rareapi.view_rareuser'):
            raise PermissionDenied()
        users = PriorityUser.objects.order_by('user__first_name').exclude(user=request.user).exclude(user__is_active=True)
        serializer = PriorityUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=["post", "delete" ], detail=False)
    def subscription(self, request):
        author = PriorityUser.objects.get(pk=request.data["author_id"])
        follower = PriorityUser.objects.get(user=request.auth.user)

        if request.method == "POST":
            subscription = Subscription()
            subscription.author = author
            subscription.follower = follower
            try:
                subscription.save()
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception:
                return HttpResponseServerError(Exception)
        elif request.method == "DELETE":
            try:
                subscription = Subscription.objects.get(author=author, follower=follower, ended_on=None)
                subscription.ended_on = timezone.now()
                subscription.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Exception:
                return HttpResponseServerError(Exception)
    
    @action(methods=["post"], detail=False)
    def subscription_status(self, request):
        author = PriorityUser.objects.get(pk=request.data["author_id"])
        follower = PriorityUser.objects.get(user=request.auth.user)

        try:
            subscription = Subscription.objects.get(author=author, follower=follower, ended_on=None)
            response = json.dumps({"subscribed": True})
            return HttpResponse(response, content_type='application/json')
        except:
            response = json.dumps({"subscribed": False})
            return HttpResponse(response, content_type='application/json')
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

class WhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = What
        fields = ('id', 'priority', 'what', 'is_deleted')

class HistorySerializer(serializers.ModelSerializer):
    what = WhatSerializer(many=False)
    class Meta:
        model = History
        fields = ('id', 'what', 'submission_date', 'goal_date', 'time_spent')
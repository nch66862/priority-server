from django.http.response import HttpResponse
from priorityapi.models import PriorityUser, What, Priority
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class WhatViewSet(ViewSet):
    def list(self, request):
        user = PriorityUser.objects.get(user=request.auth.user)
        whats = What.objects.filter(priority__priority_user=user, is_deleted=False)
        serializer = WhatSerializer(whats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk):
        priority = Priority.objects.get(pk=pk)
        user = PriorityUser.objects.get(pk=priority.priority_user_id)
        whats = What.objects.filter(priority__priority_user=user, is_deleted=False)
        serializer = WhatSerializer(whats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        what = What()
        what.priority_id = request.data['priority_id']
        what.what = request.data['what']
        what.save()
        serializer = WhatSerializer(what, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        what = What.objects.get(pk=pk)
        what.is_deleted = True
        what.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
class WhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = What
        fields = ('id', 'priority', 'what', 'is_deleted')
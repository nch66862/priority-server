from django.http.response import HttpResponse
from priorityapi.models import PriorityUser, What
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class WhatViewSet(ViewSet):
    def list(self, request):
        user = PriorityUser.objects.get(user=request.auth.user)
        whats = What.objects.filter(priority__priority_user=user)
        serializer = WhatSerializer(whats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class WhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = What
        fields = ('id', 'priority', 'what', 'is_deleted')
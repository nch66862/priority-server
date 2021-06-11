from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from priorityapi.models import PriorityUser
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

@api_view()
def check_active(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''
    priority_user = PriorityUser.objects.get(user = request.auth.user)
    data = json.dumps({"is_active": request.auth.user.is_active, "is_admin": request.auth.user.is_staff, "logged_in_user_id": priority_user.id})
    return HttpResponse(data, content_type='application/json')
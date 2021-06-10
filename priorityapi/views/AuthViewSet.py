import json
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rareapi.models import RareUser
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile
import base64
import uuid

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a rare user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        email=req_body['email'],
        password=req_body['password'],
        is_staff=True
    )

    # Now save the extra info in the levelupapi_gamer table

    rare_user = RareUser.objects.create(
        bio=req_body['bio'],
        user=new_user
    )
    if req_body["profile_image_url"] == "":
        rare_user.profile_image = "profile_images/12-f992eaef-09f3-40e0-8da0-39817f4fab3a.jpeg"
    else:
        format, imgstr = req_body["profile_image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{rare_user.id}-{uuid.uuid4()}.{ext}')

        rare_user.profile_image = data
    rare_user.save()

    #Give user default permissions
    permissions = [46, 48, 33, 34, 35, 49, 50, 51, 57, 58, 59]
    new_user.user_permissions.set(permissions)

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"valid": True, "token": token.key})
    return HttpResponse(data, content_type='application/json')
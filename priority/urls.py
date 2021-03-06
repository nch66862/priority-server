"""priority URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from priorityapi.views import register_user, login_user, check_active, PriorityUserViewSet, WhatViewSet, HistoryViewSet, PriorityViewSet, AffirmationViewSet, SubscriptionViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', PriorityUserViewSet, 'user')
router.register(r'what', WhatViewSet, 'what')
router.register(r'history', HistoryViewSet, 'history')
router.register(r'priority', PriorityViewSet, 'priority')
router.register(r'affirmations', AffirmationViewSet, 'affirmation')
router.register(r'subscriptions', SubscriptionViewSet, 'subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('check-active', check_active),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

]

#!/usr/bin/env python

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewset

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'v1/structures/', viewset.StructureViewSet.as_view(), name='structure'),
    path(r'v1/structures/<str:id>/', viewset.StructureViewIDSet.as_view(), name='structureid'),

]

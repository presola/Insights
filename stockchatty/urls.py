#!/usr/bin/env python

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from graphene_django.views import GraphQLView

router = DefaultRouter()

urlpatterns = [
    path(r'graphene', GraphQLView.as_view(graphiql=True), name='stock'),
    path(r'api/', GraphQLView.as_view(graphiql=False), name='stock'),

]

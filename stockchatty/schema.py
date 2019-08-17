from django.db import models

from graphene_django import DjangoObjectType
import graphene
from .models import StockModel
# Create your models here.
from .views import get_data


class Stocks(DjangoObjectType):
    class Meta:
        model = StockModel
        # filter_fields = ["symbol", "no_of_days"]

class Query(graphene.ObjectType):
    stocks = graphene.List(Stocks, symbol=graphene.String(), days=graphene.Int())

    def resolve_stocks(self, info, **kwargs):
        return get_data(kwargs)

schema = graphene.Schema(query=Query)

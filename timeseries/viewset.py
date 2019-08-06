#!/usr/bin/env python

from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.response import Response
import coreapi
import coreschema
from rest_framework.schemas import ManualSchema
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .views import process_structure
from django.http import JsonResponse

class PriceViewSet(ModelViewSet):
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE')
    queryset = Prices.objects.all()
    serializer_class = PricesSerializer


class StructurePricesViewSet(ModelViewSet):
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE')
    queryset = Structure.objects.all()
    serializer_class = StructurePricesSerializer


class StructurePricesMetaViewSet(ModelViewSet):
    allowed_methods = ('GET', 'DELETE')
    queryset = Structure.objects.all()
    serializer_class = StructurePricesMetaSerializer


get_extra_fields = [
    coreapi.Field(
        "id",
        required=True,
        location="path",
        example="1",
        description='ID of structure',
        schema=coreschema.String()
    ),
]
post_extra_fields = [
    coreapi.Field(
        "id",
        required=True,
        location="path",
        example="1",
        description='ID of structure',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "predict",
        required=True,
        location="form",
        example="false",
        description='For Prediction or Filtering',
        schema=coreschema.Boolean()
    ),
    coreapi.Field(
        "State",
        required=False,
        location="form",
        example="false",
        description='state to filter by',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "Metro",
        required=True,
        location="form",
        description='metro to filter by',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "CountyName",
        required=True,
        location="form",
        description='county to filter by',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "start_date",
        required=True,
        location="form",
        description='start date',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "end_date",
        required=True,
        location="form",
        description='end date',
        schema=coreschema.String()
    ),
]

class CustomIDSchema(ManualSchema):
    """
    Overrides `get_link()` to provide Custom Behavior X
    """
    def get_link(self, path, method, base_url):
        if method == 'POST':
            self._fields = post_extra_fields
        if method == 'GET':
            self._fields = get_extra_fields
        link = super().get_link(path, method, base_url)
        # Do something to customize link here...
        return link

def verify_data():
    strucs = Structure.objects.count()
    if strucs < 3:
        from timeseries.functions import load
    prices = Prices.objects.count()
    if prices < 3:
        Structure.objects.delete()
        from timeseries.functions import load
    

def get_struc(kwargs):
    verify_data()
    if 'id' in kwargs:
        strucs = Structure.objects.filter(id=kwargs["id"]).get()
        serializer = StructurePricesSerializer(strucs, many=False)
    else:
        strucs = Structure.objects.all()
        serializer = StructurePricesMetaSerializer(strucs, many=True)
    return JsonResponse(serializer.data, safe=False)

class StructureViewSet(APIView):
    """
    get:
        Get all available structures
    """
    queryset = Structure.objects.all()
    permission_classes = [AllowAny]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return get_struc(kwargs)


class StructureViewIDSet(APIView):
    """

    get:
        Get structure by id
    post:
        Filter by or Predict Structures
    """
    queryset = Structure.objects.all()
    permission_classes = [AllowAny]
    schema = CustomIDSchema(fields=[])

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return get_struc(kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return process_structure(request, kwargs["id"])

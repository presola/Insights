#!/usr/bin/env python

from rest_framework import serializers
from .models import *
from operator import itemgetter
from django.db import transaction
from .functions.general import format_structures

class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ('id', 'name', 'csv_title', 'key','start_date', 'end_date',)

class PricesMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('id', 'RegionName', 'State', 'Metro', 'CountyName', 'SizeRank','start_date', 'end_date', )


class PricesSerializer(serializers.ModelSerializer):
    HousePrices = serializers.SerializerMethodField()


    class Meta:
        model = Prices
        fields = ('id', 'RegionName', 'State', 'Metro', 'CountyName', 'SizeRank', 'start_date', 'end_date', 'HousePrices', )

    def get_HousePrices(self, json):
        # return json.HousePrices[:10]
        return json.HousePrices

class StructurePricesMetaSerializer(serializers.ModelSerializer):
    structure_prices = PricesMetaSerializer(many=True)
    # structure_prices = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = ('id', 'name', 'csv_title', 'key','start_date', 'end_date', 'structure_prices',)

    # def get_structure_prices(self, json):
    #     prices = json.structure_prices
    #     return_dict = dict()
    #     return_dict['regions'] = [item['RegionName'] for item in prices]
    #     return_dict['states'] = [item['State'] for item in prices]
    #     return_dict['metros'] = [item['Metro'] for item in prices]
    #     return_dict['counties'] = [item['CountyName'] for item in prices]
    #     return return_dict

class StructurePricesSerializer(serializers.ModelSerializer):
    # structure_prices = PricesSerializer(many=True)
    structure_prices = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = ('id', 'name', 'csv_title', 'key','start_date', 'end_date', 'structure_prices',)

    def get_structure_prices(self, json):

        structure_prices = PricesSerializer(json.structure_prices.all(), many=True).data
        new_list = format_structures(structure_prices)
        return new_list

    def create(self, validated_data):
        price_data = validated_data.pop('prices')
        price_template = Structure.objects.create(**validated_data)

        for price in price_data:
            Prices.objects.create(structure=price_template, **price)

        return price_template

    def update(self, instance, validated_data):
        with transaction.atomic():
            # ['RegionName', 'State', 'Metro', 'CountyName', 'SizeRank', 'HousePrices']
            if 'RegionName' in validated_data:
                instance.RegionName = validated_data['RegionName']
            if 'State' in validated_data:
                instance.State = validated_data['State']
            if 'Metro' in validated_data:
                instance.Metro = validated_data['Metro']
            if 'CountyName' in validated_data:
                instance.CountyName = validated_data['CountyName']
            if 'SizeRank' in validated_data:
                instance.SizeRank = validated_data['SizeRank']
            if 'HousePrices' in validated_data:
                instance.HousePrices = validated_data['HousePrices']

            instance.save()
            price_data = validated_data.pop('prices')
            for price in price_data:
                Prices.objects.create(structure=instance, **price)


        return instance
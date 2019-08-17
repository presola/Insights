from django.db import models

# Create your models here.

class StockModel(models.Model):
    Volume = models.BigIntegerField(default=0.0)
    Days = models.IntegerField(default=0)
    Symbol = models.CharField(max_length=100)
    High = models.FloatField(default=0.0)
    Low = models.FloatField(default=0.0)
    Date = models.BigIntegerField(default=0.0)
    Open = models.FloatField(default=0.0)
    Close = models.FloatField(default=0.0)

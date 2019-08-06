from django.db import models
import jsonfield

# Create your models here.

class Structure(models.Model):
    name = models.TextField()
    csv_title = models.TextField()
    key = models.TextField()
    start_date = models.TextField()
    end_date = models.TextField()


    def delete(self, *args, **kwargs):
        super(Structure, self).delete(*args, **kwargs)

class Prices(models.Model):
    structure = models.ForeignKey(Structure, related_name='structure_prices', on_delete=models.CASCADE)
    RegionName = models.TextField()
    State = models.TextField()
    Metro = models.TextField()
    CountyName = models.TextField()
    SizeRank = models.TextField()
    start_date = models.TextField()
    end_date = models.TextField()
    HousePrices = jsonfield.JSONField(default=[])

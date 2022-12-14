from django.db import models

# Create your models here.


class Data(models.Model):
    datetime = models.DateTimeField()
    close = models.DecimalField(max_digits=5, decimal_places=2)
    high = models.DecimalField(max_digits=5, decimal_places=2)
    low = models.DecimalField(max_digits=5, decimal_places=2)
    open = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.BigIntegerField()
    instrument = models.TextField(max_length=255)

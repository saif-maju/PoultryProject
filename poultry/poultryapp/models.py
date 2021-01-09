from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500)
    price = models.FloatField()
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    eod_date = models.DateField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name        

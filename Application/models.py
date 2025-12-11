from django.db import models

# Create your models here.
class Search(models.Model):
    city = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=True)
    venue = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    cityState = models.CharField(max_length=30,null=True)
    date = models.CharField(max_length=50,null=True)
    time = models.CharField(max_length=30,null=True)
    priceMin = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    priceMax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    url = models.URLField(null=True)
    imgUrl = models.URLField(null=True)

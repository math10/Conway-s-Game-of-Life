from django.db import models

# Create your models here.
class Grid(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    data = models.TextField(null=False)
from django.db import models


# Create your models here.
class ShortComment(models.Model):

    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=200)
    stars = models.CharField(max_length=5)
    ts = models.DateTimeField()

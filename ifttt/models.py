from django.db import models


# Create your models here.
class Clause(models.Model):
    user = models.CharField(null=True)
    key = models.CharField(null=True)
    state = models.CharField(null=True)


class Event(models.Model):
    timestamp = models.DateTimeField(null=True)

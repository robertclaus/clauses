from django.db import models


# Create your models here.
class Clause(models.Model):
    user = models.TextField(null=True, blank=True)
    key = models.TextField(null=True)
    state = models.TextField(null=True)


class Event(models.Model):
    timestamp = models.DateTimeField(null=True)
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE)

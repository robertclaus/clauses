from django.db import models


# Create your models here.
class Clause(models.Model):
    user = models.TextField(null=True, blank=True)
    key = models.TextField(null=True)
    state = models.TextField(null=True)
    last_true = models.BooleanField(default=False)


class Event(models.Model):
    timestamp = models.DateTimeField(null=True)
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE, null=True)


class Trigger(models.Model):
    last_code = models.CharField(max_length=5000, null=True, blank=True)
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE, null=True)
    trigger_identity = models.CharField(max_length=5000, null=True, blank=True)

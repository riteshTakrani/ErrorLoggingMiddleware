from django.db import models


class ResponseModel(models.Model):
    status = models.IntegerField()
    error = models.CharField(max_length=128)
    entry_date = models.DateTimeField()

    def __str__(self):
        return str(self.status)

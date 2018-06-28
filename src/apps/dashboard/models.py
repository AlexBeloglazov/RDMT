from django.db import models


class UnresolvedDocument(models.Model):

    name = models.CharField(max_length=255)
    content = models.TextField()
    region = models.CharField(max_length=100)
    lob = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

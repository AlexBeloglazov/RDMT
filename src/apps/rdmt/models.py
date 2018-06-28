from django.db import models


class Classifier(models.Model):
    """
    Model for BLOBed classifiers
    """

    regions = {
        'APAC': ('', 0),
        'EMEA': ('', 1),
        'NAMR': ('', 2),
        'Unknown': ('', 3)
    }

    lobs = {
        'Commercial Lending': ('', 0),
        'Consumer Lending': ('', 1),
        'Credit Cards': ('', 2),
        'Investment Banking': ('', 3),
        'Unknown': ('', 4)
    }

    categories = {
        'Regulation A': ('', 0),
        'Regulation B': ('', 1),
        'Regulation C': ('', 2),
        'Regulation D': ('', 3),
        'Unknown': ('', 4)
    }

    accuracy = models.FloatField()

    region = models.BinaryField()
    lob = models.BinaryField()
    category = models.BinaryField()

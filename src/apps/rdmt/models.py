from django.db import models


class Classifier(models.Model):
    """
    Model for BLOBed classifier
    """

    classes = {
        'ClassA': ('', 0),
        'ClassB': ('', 1),
        'ClassC': ('', 2),
        'ClassD': ('', 3),
        'ClassUnknown': ('', 4)
    }

    classifier = models.BinaryField()

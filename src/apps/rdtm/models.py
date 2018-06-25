from django.db import models


class Classifier(models.Model):
    """
    Model pickled classifier
    """

    classes = {
        'ClassA': ('', 0),
        'ClassB': ('', 1),
        'ClassC': ('', 2),
    }

    classifier = models.BinaryField()

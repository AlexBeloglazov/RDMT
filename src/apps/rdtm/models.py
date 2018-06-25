from django.db import models


class HyperParamters(models.Model):
    """
    Model stores hyper parameters of the classificator
    """

    classes = {
        'ClassA': 0,
        'ClassB': 1,
        'ClassC': 2,
    }

    parameters = models.TextField()

from django.db import models

# Create your models here.
class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    objects = models.Manager()

    def __str__(self):
        return str(self.name) + " : " + str(self.description)

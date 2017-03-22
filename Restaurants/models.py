from django.db import models

class Recommendation(models.Model):
    name = models.CharField(max_length = 100)
    locationX =  models.DecimalField(max_digits = 12, decimal_places = 9)
    locationY = models.DecimalField(max_digits = 12, decimal_places = 9)
    cost = models.IntegerField()
    rating = models.DecimalField(max_digits = 2, decimal_places = 1)
    picture = models.CharField(max_length = 2000)

    def __str__(self):
        return self.name
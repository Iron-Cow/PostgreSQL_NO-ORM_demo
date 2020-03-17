from django.db import models

# Create your models here.


class Gender(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name}"


class Human(models.Model):
    name = models.CharField(max_length=48)
    age = models.IntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

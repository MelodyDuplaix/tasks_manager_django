from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class SubManager(models.Model):
    name = models.fields.CharField(max_length=500)
    daily_objectif = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], default=10)
    weekly_objectif = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], default=50)
    monthly_objectif = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], default=200)

    def __str__(self):
        return f"{self.name}"

class TaskType(models.Model):
    name = models.CharField(max_length=255)
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"

class Task(models.Model):
    name = models.fields.CharField(max_length=500)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    ponctuel = models.fields.BooleanField(default=False)
    type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"

class Reward(models.Model):
    name = models.fields.CharField(max_length=500)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"

class Action(models.Model):
    name = models.fields.CharField(max_length=500)
    date = models.fields.DateTimeField(default=timezone.now)
    type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"

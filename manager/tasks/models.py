from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class SubManager(models.Model):
    name = models.fields.CharField(max_length=500)

class TaskType(models.Model):
    name = models.CharField(max_length=255)
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

class task(models.Model):
    name = models.fields.CharField(max_length=500)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    ponctuel = models.fields.BooleanField(default=False)
    type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

class Reward(models.Model):
    name = models.fields.CharField(max_length=500)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

class Action(models.Model):
    name = models.fields.CharField(max_length=500)
    date = models.fields.DateTimeField(default=timezone.now)
    type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)

class Objectif(models.Model):
    name = models.fields.CharField(max_length=500)
    coins_number = models.fields.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    sub_manager = models.ForeignKey(SubManager, null=True, on_delete=models.SET_NULL)
# Generated by Django 5.1.3 on 2024-12-02 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_submanager_daily_objectif_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Objectif',
        ),
    ]
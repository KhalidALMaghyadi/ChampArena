# Generated by Django 5.1.4 on 2024-12-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='longitude',
            field=models.FloatField(),
        ),
    ]

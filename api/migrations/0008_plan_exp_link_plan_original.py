# Generated by Django 4.2.5 on 2023-09-20 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_userplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='exp_link',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='original',
            field=models.BooleanField(default=False),
        ),
    ]

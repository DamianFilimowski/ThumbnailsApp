# Generated by Django 4.2.5 on 2023-09-20 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_thumbnailsize_plan_sizes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thumbnailsize',
            old_name='size',
            new_name='height',
        ),
    ]

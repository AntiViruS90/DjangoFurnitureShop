# Generated by Django 4.2.10 on 2024-02-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0014_rename_additionalphoto_additionalphotos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalphotos',
            name='image',
            field=models.CharField(max_length=20),
        ),
    ]

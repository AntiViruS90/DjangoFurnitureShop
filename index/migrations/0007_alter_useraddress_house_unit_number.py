# Generated by Django 5.0.2 on 2024-02-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_alter_useraddress_house_unit_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='house_unit_number',
            field=models.IntegerField(blank=True),
        ),
    ]
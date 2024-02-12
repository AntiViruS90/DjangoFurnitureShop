# Generated by Django 5.0.2 on 2024-02-11 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_alter_user_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='house_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='house_unit_number',
            field=models.IntegerField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='post_code',
            field=models.IntegerField(max_length=30),
        ),
    ]
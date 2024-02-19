# Generated by Django 4.2.10 on 2024-02-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_remove_product_additional_photos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='additional_photos')),
            ],
        ),
        migrations.DeleteModel(
            name='AdditionalPhotos',
        ),
        migrations.AlterField(
            model_name='product',
            name='additional_photos',
            field=models.ManyToManyField(blank=True, to='index.additionalphoto'),
        ),
    ]
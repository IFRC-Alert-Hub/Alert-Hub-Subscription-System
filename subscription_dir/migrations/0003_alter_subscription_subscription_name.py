# Generated by Django 4.2.2 on 2023-08-25 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_dir', '0002_remove_subscription_district_ids_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='subscription_name',
            field=models.CharField(default='', max_length=512, verbose_name='subscription_name'),
        ),
    ]

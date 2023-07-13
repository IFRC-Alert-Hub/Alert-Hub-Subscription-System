# Generated by Django 4.2.2 on 2023-06-19 20:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0003_remove_alert_areadesc_remove_alert_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None')),
                ('polygon', models.CharField(default='None')),
                ('centroid', models.CharField(default='None')),
            ],
        ),
        migrations.AlterField(
            model_name='alertinfo',
            name='effective',
            field=models.CharField(default=datetime.datetime(2023, 6, 19, 20, 37, 4, 47471, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='alertinfo',
            name='polygon',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None')),
                ('society_name', models.CharField(default='None')),
                ('polygon', models.CharField(default='None')),
                ('centroid', models.CharField(default='None')),
                ('region_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_id', to='filter.region')),
            ],
        ),
    ]
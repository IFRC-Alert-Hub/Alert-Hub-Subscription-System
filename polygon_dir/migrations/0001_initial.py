# Generated by Django 4.2.2 on 2023-07-18 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Polygon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(default=0, verbose_name='user_id')),
                ('vertices', models.CharField(default='None')),
            ],
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-16 20:19
import os

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ('subscription_manager_dir', '0002_subscriptionalerts_sent'),
    ]
    if os.environ["Test_Environment"] == 'True':

        operations = [
            migrations.CreateModel(
                name='CapFeedCountry',
                fields=[
                    ('id', models.BigAutoField(primary_key=True, serialize=False)),
                    ('name', models.CharField(max_length=255)),
                ],
                options={
                    'db_table': 'cap_feed_country',
                    'managed': True,
                },
            ),
            migrations.CreateModel(
                name='CapFeedAdmin1',
                fields=[
                    ('id', models.BigAutoField(primary_key=True, serialize=False)),
                    ('name', models.CharField(max_length=255)),
                ],
                options={
                    'db_table': 'cap_feed_admin1',
                    'managed': True,
                },
            ),
            migrations.CreateModel(
                name='CapFeedAlert',
                fields=[
                    ('id', models.BigAutoField(primary_key=True, serialize=False)),
                    ('sent', models.DateTimeField()),
                ],
                options={
                    'db_table': 'cap_feed_alert',
                    'managed': True,
                },
            ),
            migrations.CreateModel(
                name='CapFeedAlertinfo',
                fields=[
                    ('id', models.BigAutoField(primary_key=True, serialize=False)),
                    ('category', models.CharField()),
                    ('event', models.CharField(max_length=255)),
                    ('urgency', models.CharField()),
                    ('severity', models.CharField()),
                    ('certainty', models.CharField()),
                    ('alert', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subscription_manager_dir.capfeedalert')),
                ],
                options={
                    'db_table': 'cap_feed_alertinfo',
                    'managed': True,
                },
            ),
            migrations.CreateModel(
                name='CapFeedAlertadmin1',
                fields=[
                    ('id', models.BigAutoField(primary_key=True, serialize=False)),
                    ('admin1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subscription_manager_dir.capfeedadmin1')),
                    ('alert', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subscription_manager_dir.capfeedalert')),
                ],
                options={
                    'db_table': 'cap_feed_alertadmin1',
                    'managed': True,
                },
            ),
            migrations.AddField(
                model_name='capfeedalert',
                name='admin1s',
                field=models.ManyToManyField(through='subscription_manager_dir.CapFeedAlertadmin1', to='subscription_manager_dir.capfeedadmin1'),
            ),
            migrations.AddField(
                model_name='capfeedalert',
                name='country',
                field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subscription_manager_dir.capfeedcountry'),
            ),
            migrations.AddField(
                model_name='capfeedadmin1',
                name='country',
                field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subscription_manager_dir.capfeedcountry'),
            )
        ]
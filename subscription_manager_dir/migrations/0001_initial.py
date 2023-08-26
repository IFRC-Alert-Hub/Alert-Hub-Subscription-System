# Generated by Django 4.2.3 on 2023-08-09 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscription_dir', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapFeedAdmin1',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cap_feed_admin1',
                'managed': False,
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
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CapFeedAlertadmin1',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'cap_feed_alertadmin1',
                'managed': False,
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
            ],
            options={
                'db_table': 'cap_feed_alertinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CapFeedCountry',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cap_feed_country',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionAlerts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription_manager_dir.alert')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription_dir.subscription')),
            ],
        ),
        migrations.AddField(
            model_name='alert',
            name='subscriptions',
            field=models.ManyToManyField(through='subscription_manager_dir.SubscriptionAlerts', to='subscription_dir.subscription'),
        ),
    ]
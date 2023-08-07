# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CapFeedAdmin1(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    polygon = models.TextField(blank=True, null=True)
    multipolygon = models.TextField(blank=True, null=True)
    min_latitude = models.FloatField(blank=True, null=True)
    max_latitude = models.FloatField(blank=True, null=True)
    min_longitude = models.FloatField(blank=True, null=True)
    max_longitude = models.FloatField(blank=True, null=True)
    country = models.ForeignKey('CapFeedCountry', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_admin1'


class CapFeedAlert(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(unique=True, max_length=255)
    identifier = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    sent = models.DateTimeField()
    status = models.CharField()
    msg_type = models.CharField()
    source = models.CharField(max_length=255)
    scope = models.CharField()
    restriction = models.CharField(max_length=255)
    addresses = models.TextField()
    code = models.CharField(max_length=255)
    note = models.TextField()
    references = models.TextField()
    incidents = models.TextField()
    country = models.ForeignKey('CapFeedCountry', models.DO_NOTHING)
    feed = models.ForeignKey('CapFeedFeed', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alert'


class CapFeedAlertadmin1(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin1 = models.ForeignKey(CapFeedAdmin1, models.DO_NOTHING)
    alert = models.ForeignKey(CapFeedAlert, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertadmin1'


class CapFeedAlertinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    language = models.CharField(max_length=255)
    category = models.CharField()
    event = models.CharField(max_length=255)
    response_type = models.CharField()
    urgency = models.CharField()
    severity = models.CharField()
    certainty = models.CharField()
    audience = models.CharField()
    event_code = models.CharField(max_length=255)
    effective = models.DateTimeField()
    onset = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField()
    sender_name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=255)
    parameter = models.CharField(max_length=255)
    alert = models.ForeignKey(CapFeedAlert, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfo'


class CapFeedAlertinfoarea(models.Model):
    id = models.BigAutoField(primary_key=True)
    area_desc = models.TextField()
    altitude = models.CharField()
    ceiling = models.CharField()
    alert_info = models.ForeignKey(CapFeedAlertinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfoarea'


class CapFeedAlertinfoareacircle(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.TextField()
    alert_info_area = models.ForeignKey(CapFeedAlertinfoarea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfoareacircle'


class CapFeedAlertinfoareageocode(models.Model):
    id = models.BigAutoField(primary_key=True)
    value_name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    alert_info_area = models.ForeignKey(CapFeedAlertinfoarea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfoareageocode'


class CapFeedAlertinfoareapolygon(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.TextField()
    alert_info_area = models.ForeignKey(CapFeedAlertinfoarea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfoareapolygon'


class CapFeedAlertinfoparameter(models.Model):
    id = models.BigAutoField(primary_key=True)
    value_name = models.CharField(max_length=255)
    value = models.TextField()
    alert_info = models.ForeignKey(CapFeedAlertinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfoparameter'


class CapFeedContinent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cap_feed_continent'


class CapFeedCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    iso3 = models.CharField(unique=True)
    polygon = models.TextField(blank=True, null=True)
    multipolygon = models.TextField(blank=True, null=True)
    centroid = models.CharField(max_length=255, blank=True, null=True)
    continent = models.ForeignKey(CapFeedContinent, models.DO_NOTHING)
    region = models.ForeignKey('CapFeedRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_country'


class CapFeedFeed(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(unique=True, max_length=255)
    format = models.CharField()
    polling_interval = models.IntegerField()
    official = models.BooleanField()
    status = models.CharField()
    author_name = models.CharField()
    author_email = models.CharField()
    notes = models.TextField()
    country = models.ForeignKey(CapFeedCountry, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_feed'


class CapFeedFeedlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    exception = models.CharField(max_length=255)
    error_message = models.TextField()
    description = models.TextField()
    response = models.TextField()
    alert_url = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    notes = models.TextField()
    feed = models.ForeignKey(CapFeedFeed, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_feedlog'
        unique_together = (('alert_url', 'description'),)


class CapFeedLanguageinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    language = models.CharField()
    logo = models.CharField(max_length=255, blank=True, null=True)
    feed = models.ForeignKey(CapFeedFeed, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_languageinfo'


class CapFeedRegion(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    polygon = models.TextField(blank=True, null=True)
    centroid = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cap_feed_region'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoCeleryResultsChordcounter(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    sub_tasks = models.TextField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_chordcounter'


class DjangoCeleryResultsGroupresult(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    date_created = models.DateTimeField()
    date_done = models.DateTimeField()
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_groupresult'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()
    periodic_task_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

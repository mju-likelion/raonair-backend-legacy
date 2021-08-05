# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
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


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    play = models.ForeignKey('Play', models.DO_NOTHING, db_column='play')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')

    class Meta:
        managed = False
        db_table = 'comment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

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


class Like(models.Model):
    play = models.ForeignKey('Play', models.DO_NOTHING, db_column='play')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')

    class Meta:
        managed = False
        db_table = 'like'


class Person(models.Model):
    name = models.CharField(max_length=255)
    photo = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'

class Play(models.Model):
    title = models.CharField(max_length=255)
    poster = models.CharField(unique=True, max_length=255)
    start_date = models.DateField(db_column='start_DATE')  # Field name made lowercase.
    end_date = models.DateField(db_column='end_DATE', blank=True, null=True)  # Field name made lowercase.
    running_time = models.IntegerField()
    troupe = models.ForeignKey('Troupe', models.DO_NOTHING, db_column='troupe')
    theater = models.ForeignKey('Theater', models.DO_NOTHING, db_column='theater')
    yes24_external_link = models.CharField(unique=True, max_length=255, blank=True, null=True)
    interpark_external_link = models.CharField(unique=True, max_length=255, blank=True, null=True)
    playdb_external_link = models.CharField(db_column='playDB_external_link', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    culturegov_external_link = models.CharField(db_column='cultureGov_external_link', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'play'


class Staff(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person', blank=True, null=True)
    play = models.ForeignKey(Play, models.DO_NOTHING, db_column='play', blank=True, null=True)
    role = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'staff'


class Star(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    play = models.ForeignKey(Play, models.DO_NOTHING, db_column='play')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')

    class Meta:
        managed = False
        db_table = 'star'


class Team(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person', blank=True, null=True)
    troupe = models.ForeignKey('Troupe', models.DO_NOTHING, db_column='troupe', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'

class Theater(models.Model):
    name = models.CharField(unique=True, max_length=255)
    address = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'theater'


class Troupe(models.Model):
    name = models.CharField(unique=True, max_length=255)
    type = models.CharField(max_length=7)
    logo = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'troupe'


class TroupeLike(models.Model):
    troupe = models.ForeignKey(Troupe, models.DO_NOTHING, db_column='troupe', blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'troupe_like'


class User(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=10)
    nickname = models.CharField(unique=True, max_length=10)
    email_confirmed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'

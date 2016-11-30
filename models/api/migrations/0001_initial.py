# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('userid', models.CharField(max_length=24)),
                ('auth', models.CharField(serialize=False, unique=True, max_length=96, primary_key=True)),
                ('user_type', models.SmallIntegerField(default=0)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('mnemonic', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=4)),
                ('section', models.CharField(blank=True, max_length=3)),
                ('id', models.CharField(serialize=False, unique=True, max_length=5, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('website', models.URLField(default='', blank=True)),
                ('meet_time', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('max_students', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['mnemonic', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('enroll_status', models.CharField(choices=[('E', 'Enrolled'), ('W', 'Waitlisted'), ('D', 'Dropped'), ('P', 'Planned')], max_length=1)),
                ('course', models.ForeignKey(to='api.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('id', models.CharField(serialize=False, unique=True, max_length=6, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=24)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id', 'last_name', 'first_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('id', models.CharField(serialize=False, unique=True, max_length=6, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=24)),
                ('password', models.CharField(max_length=100)),
                ('taking_courses', models.ManyToManyField(to='api.Course', blank=True, through='api.Enrollment')),
            ],
            options={
                'ordering': ['id', 'last_name', 'first_name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(to='api.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(to='api.Instructor'),
        ),
    ]

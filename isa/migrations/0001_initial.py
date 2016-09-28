# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('mnemonic', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=4)),
                ('section', models.CharField(max_length=3, blank=True)),
                ('id', models.IntegerField(serialize=False, unique=True, default=0, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
                ('website', models.URLField(blank=True, default='')),
                ('meet_time', models.CharField(max_length=100, blank=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('max_students', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['mnemonic', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enroll_status', models.CharField(max_length=1, choices=[('E', 'Enrolled'), ('W', 'Waitlisted'), ('D', 'Dropped'), ('P', 'Planned')])),
                ('course', models.ForeignKey(to='isa.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('id', models.CharField(serialize=False, max_length=6, unique=True, primary_key=True)),
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
                ('id', models.CharField(serialize=False, max_length=6, unique=True, primary_key=True)),
                ('taking_courses', models.ManyToManyField(to='isa.Course', through='isa.Enrollment', blank=True)),
            ],
            options={
                'ordering': ['id', 'last_name', 'first_name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(to='isa.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(to='isa.Instructor'),
        ),
    ]

from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id = models.CharField(max_length=6, unique=True, primary_key=True)

    class Meta:
        abstract = True
        ordering = ['id', 'last_name', 'first_name']


class Instructor(Profile):
    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        instructor_id = '(' + self.id + ')'
        return name + ' ' + instructor_id


class Course(models.Model):
    mnemonic = models.CharField(max_length=4)
    number = models.CharField(max_length=4)
    section = models.CharField(max_length=3, blank=True)
    id = models.CharField(unique=True, primary_key=True)

    instructor = models.ForeignKey('Instructor')
    title = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, default='')

    meet_time = models.CharField(blank=True, max_length=100)
    location = models.CharField(blank=True, max_length=100)
    max_students = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.mnemonic + ' ' + str(self.number)

    class Meta:
        ordering = ['mnemonic', 'number']


class Student(Profile):
    taking_courses = models.ManyToManyField('Course', through='Enrollment', blank=True)

    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        student_id = '(' + self.id + ')'
        return name + ' ' + student_id


class Enrollment(models.Model):
    course = models.ForeignKey('Course')
    student = models.ForeignKey('Student')

    STATUS = (
        ('E', 'Enrolled'),
        ('W', 'Waitlisted'),
        ('D', 'Dropped'),
        ('P', 'Planned'),
    )
    enroll_status = models.CharField(max_length=1, choices=STATUS)

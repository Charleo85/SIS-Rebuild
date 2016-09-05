from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    computing_id = models.CharField(max_length=6)

    class Meta:
        abstract = True
        ordering = ['computing_id', 'last_name', 'first_name']


class Instructor(Profile):
    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        instructor_id = '(' + self.computing_id + ')'
        return name + ' ' + instructor_id


class Student(Profile):
    taking_courses = models.ManyToManyField(Course, through='Enrollment')

    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        student_id = '(' + self.computing_id + ')'
        return name + ' ' + student_id


class Course(models.Model):
    mnemonic = models.CharField(max_length=4)
    number = models.SmallIntegerField()
    section = models.SmallIntegerField()
    sis_id = models.IntegerField()

    instructor = models.ForeignKey(Instructor)
    title = models.CharField(max_length=100)
    description = models.TextField()

    meet_time = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    max_students = models.SmallIntegerField()

    def __str__(self):
        return self.mnemonic + ' ' + str(self.course_number)

    class Meta:
        ordering = ['mnemonic', 'number']


class Enrollment(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)

    STATUS = (
        ('E', 'Enrolled'),
        ('W', 'Waitlisted'),
        ('D', 'Dropped'),
        ('P', 'Planned'),
    )
    enroll_status = models.CharField(max_length=1, choices=STATUS)

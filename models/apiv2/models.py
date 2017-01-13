from django.db import models


class Grade(models.Model):
    average_gpa = models.DecimalField(max_digits=4, decimal_places=3, default=0, blank=True)

    num_a_plus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_a = models.PositiveSmallIntegerField(default=0)
    num_a_minus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_b_plus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_b = models.PositiveSmallIntegerField(default=0)
    num_b_minus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_c_plus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_c = models.PositiveSmallIntegerField(default=0)
    num_c_minus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_d_plus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_d = models.PositiveSmallIntegerField(default=0)
    num_d_minus = models.PositiveSmallIntegerField(default=0, blank=True)
    num_f = models.PositiveSmallIntegerField(default=0)

    num_withdraw = models.PositiveSmallIntegerField(default=0, blank=True)
    num_drop = models.PositiveSmallIntegerField(default=0, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    mnemonic = models.CharField(max_length=4)
    number = models.CharField(max_length=4)
    description = models.TextField(blank=True)
    # have to set null=True here, or there will be tons of errors in migrations
    grade = models.OneToOneField('Grade')

    def __str__(self):
        return self.mnemonic + self.number

    class Meta:
        ordering = ['mnemonic', 'number']


class Section(models.Model):
    semester = models.CharField(max_length=20)
    section_id = models.CharField(max_length=5)
    units = models.PositiveSmallIntegerField(default=0)
    sis_id = models.CharField(max_length=5)

    section_type = models.CharField(max_length=1, choices=(
        ('e', 'lecture'),
        ('b', 'lab'),
        ('d', 'discussion'),
        ('s', 'seminar'),
        ('i', 'independent_study'),
        ('o', 'other')
    ))

    title = models.CharField(max_length=100, blank=True)
    meeting_time = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    capacity = models.PositiveSmallIntegerField(default=0, blank=True)
    other_info = models.TextField(blank=True)

    course = models.ForeignKey('Course')
    instructor = models.ForeignKey('Instructor')
    grade = models.OneToOneField('Grade', blank=True, null=True)

    def __str__(self):
        return self.semester +'-'+ self.course.mnemonic + self.course.number +'-'+ self.section

    class Meta:
        ordering = ['semester', 'sis_id']


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    interested_course = models.ManyToManyField('Section', blank=True)

    def __str__(self):
        return self.username + '-' + self.name

    class Meta:
        ordering = ['username']


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    computing_id = models.CharField(max_length=6, unique=True)

    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    cell_phone = models.CharField(max_length=20, blank=True)
    other_info = models.TextField(blank=True)

    user = models.OneToOneField(User, blank=True, null=True)

    def __str__(self):
        return self.name + '-' + self.computing_id

    class Meta:
        ordering = ['computing_id']


class Authenticator(models.Model):
    userid = models.CharField(max_length=20)
    auth = models.CharField(max_length=100, primary_key=True, unique=True)
    date_created = models.DateField(auto_now_add=True)

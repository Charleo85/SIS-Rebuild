# import models.settings

from apiv2.models import *

# This is a script that tries to precompute the generic course average GPAs
# and save them to the database

all_courses = Course.objects.all()

for course in all_courses:
    generic_course_average_gpa = 0.000
    grade_sum = 0
    grade_counter = 0

    associated_sections = course.section_set.all()
    for section in associated_sections:
        section_grade = section.grade
        grade_sum += section_grade.average_gpa
        grade_counter += 1

    try:
        generic_course_average_gpa = grade_sum / grade_counter
    except ZeroDivisionError:
        generic_course_average_gpa = None



    g = Grade(average_gpa=generic_course_average_gpa)

    course.grade = g

    course.save()

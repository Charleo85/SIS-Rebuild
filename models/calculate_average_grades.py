
# TODO: This script currently does not work. An attempt was made to pipe/input-redirect the script
# TODO: into the python manage.py shell, but a mysterious "IndentationError" kills it
# TODO: As a result, each time a new semester passes and a FOIA request is made for new data,
# TODO: the code below must be manually executed in the models layer python shell started with manage.py
# TODO: Then a dumpdata needs to be run with the updated database to have fixtures with average grades.

# This code pre-computes and saves into the database all of the average grades for "generic" courses
# (based on the average grades of all of the associated Sections for a course.) This saves a significant
# amount of time (~100x speedup) since the server does not have to do this calculation on the fly.

from apiv2.models import *

all_courses = Course.objects.all()

for course in all_courses:
    grade_sum = 0
    grade_counter = 0
    associated_sections = course.section_set.all()

    for section in associated_sections:
        section_grade = section.grade
        grade_sum += section_grade.average_gpa
        grade_counter += 1
    try:
        generic_course_average_gpa = round(grade_sum / grade_counter, 3)
    except ZeroDivisionError:
        generic_course_average_gpa = None

    course.average_gpa = generic_course_average_gpa
    course.save()


# TODO: Give instructors an average grade field as well.
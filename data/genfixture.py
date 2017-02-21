import re
import json
import csv

def parse_FOIA_csv(file_to_parse):
    courses = []
    instructors = []
    sections = []
    cou = {}
    ins = {}
    grades = []

    # read data from csv
    with open(file_to_parse, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        grade_pk = 0
        course_pk = 0
        instructor_pk = 0

        for row in csvreader:
            # print(row[0])
            if row[25] == "Total":
                continue
            section = {}
            section["model"] = "apiv2.Section"
            section_fields = {}
            section_fields["semester"] = "1162" #2016Spring

            name = row[4]+row[5]
            course_id = 0
            if name in cou:
                course_id = cou[name]
            else:
                course_pk += 1
                course = {}
                course["model"] = "apiv2.Course"
                course["pk"] = course_pk
                course_id = course_pk
                course_fields = {}
                course_fields["mnemonic"] = row[4]
                course_fields["number"] = row[5]
                course_fields["name"] = row[7]
                course["fields"] = course_fields
                courses.append(course)
                cou[name] = course_id
                # course_fields["description"] = ""
            section_fields["course"] = course_id

            match = re.findall(r'([\w\.-]+)@virginia\.edu', row[3], re.IGNORECASE)
            if match:
                compid = match[0]
                instructor_id = 0
                # print(compid)
                if compid in ins:
                    instructor_id = ins[compid]
                else:
                    instructor_pk += 1
                    instructor = {}
                    instructor["model"] = "apiv2.Instructor"
                    instructor["pk"] = instructor_pk
                    instructor_id = instructor_pk
                    instructor["model"] = "apiv2.Instructor"
                    instructor_fields = {}
                    instructor_fields["computing_id"] = compid
                    instructor_fields["email"] = row[3]
                    instructor_fields["name"] = row[1] + ' ' + row[0]
                    instructor["fields"] = instructor_fields
                    instructors.append(instructor)
                    ins[compid] = instructor_id
                section_fields["instructor"] = instructor_id
            # else:
            #     print("not match")
            #     print(row[4])


            section_fields["section_id"] = row[6]
            section_fields["sis_id"] = ""
            section_fields["section_type"] = ""
            section_fields["title"] = row[7]

            try:
                float(row[9])

                if isinstance(float(row[9]), float):
                    grade = {}
                    grade_pk += 1
                    grade["model"] = "apiv2.grade"
                    grade["pk"] = grade_pk
                    grade_fields = {}
                    grade_fields["average_gpa"] = row[8]
                    grade_fields["num_a_plus"] = row[9]
                    grade_fields["num_a"] = row[10]
                    grade_fields["num_a_minus"] = row[11]
                    grade_fields["num_b_plus"] = row[12]
                    grade_fields["num_b"] = row[13]
                    grade_fields["num_b_minus"] = row[14]
                    grade_fields["num_c_plus"] = row[15]
                    grade_fields["num_c"] = row[16]
                    grade_fields["num_c_minus"] = row[17]
                    grade_fields["num_d_plus"] = row[18]
                    grade_fields["num_d"] = row[19]
                    grade_fields["num_d_minus"] = row[20]
                    grade_fields["num_f"] = row[21]
                    grade_fields["num_other"] = row[22]
                    grade_fields["num_withdraw"] = row[23]
                    grade_fields["num_drop"] = row[24]
                    grade_fields["num_total"] = row[25]
                    grade["fields"] = grade_fields
                    section_fields["grade"] = grade_pk
                    grades.append(grade)

            except ValueError:
                continue

            section['fields'] = section_fields
            sections.append(section)


    # save data into json
    output = open("Extracted_JSON/courses.json", "a")
    course_data = json.dumps(courses)
    output.write(course_data)
    output.close()

    output = open("Extracted_JSON/grades.json", "a")
    grade_data = json.dumps(grades)
    output.write(grade_data)
    output.close

    output = open("Extracted_JSON/instructors.json", "a")
    instructor_data = json.dumps(instructors)
    output.write(instructor_data)
    output.close()

    output = open("Extracted_JSON/sections.json", "a")
    section_data = json.dumps(sections)
    output.write(section_data)
    output.close()

# TODO: Use more semesters - need to first save FOIA Grades as CSVs in other directory

parse_FOIA_csv('FOIA_Grades_CSV/GradesSpring2016.csv')
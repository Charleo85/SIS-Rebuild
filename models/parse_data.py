from lxml import html
from lxml import etree
import requests
import re
import json


tabs = []
def parse_course(href):
    output = open("output.json", "w")
    course_page = requests.get('http://rabi.phys.virginia.edu/mySIS/CS2/'+href)

    tree = html.fromstring(course_page.content)

    tables = tree.xpath('//table/tr')
    CourseNum = ""
    CourseName = ""
    for table in tables:
        if (table.xpath('./td[@class="CourseNum"]') ):
            info = table.xpath('./td[@class="CourseNum"]/span/text()')[0].split()
            CourseMn = info[0]
            CourseNum = info[1]
            CourseName = table.xpath('./td[@class="CourseName"]/text()')[0]
            # print(CourseNum)
            # print(CourseName)

        # if (table.xpath('./td[@align="right"]')):
        if (table.xpath('./td/strong')):
            if (table.xpath('./td/strong')[0].text == "Lecture"):
                tab = {}
                tab["model"] = "api.Course"
                fields = {}
                fields["mnemonic"] = CourseMn
                fields["number"] = CourseNum
                fields["title"] = CourseName
                fields["id"] = int(table.xpath('./td')[0].xpath('./a[last()]/text()')[0])
                fields["section"] = table.xpath('./td')[1].text
                fields["meet_time"] = table.xpath('./td')[6].text
                fields["location"] = table.xpath('./td')[7].text

                instructor = parse_instructor(table.xpath('./td')[5].xpath('./strong/span')[0].text)
                if (instructor != "Staff"):
                    fields["instructor"] = instructor #escape the staff case
                else:
                    continue
                tab["fields"] = fields
                # print(tab)
                tabs.append(tab)

    json_data = json.dumps(ins+tabs)
    output.write(json_data)
    output.close()

instructors = set()
ins = []
def parse_instructor(name):
    instructor_page = requests.get('http://rabi.phys.virginia.edu/mySIS/CS2/ldap.php?Name='+name)

    content = instructor_page.text
    match = re.findall(r'([\w\.-]+)@virginia\.edu', content, re.IGNORECASE)
    if (match):
        id = match[0]
        if not(id in instructors):
            tab = {}
            tab["model"] = "api.Instructor"
            fields = {}
            info = name.split()
            fields["first_name"] = info[0]
            fields["last_name"] = info[1]
            fields["id"] = match[0]
            fields["username"] = match[0]
            fields["password"] = "pbkdf2_sha256$20000$guFPvWv5N43G$VID/F7KQwoK5oUAj1JwmIGbnWHLPMLvalW8kmAQAoXA="
            tab["fields"] = fields
            # print(tab)
            ins.append(tab)
            instructors.add(id)
        return id
    else:
        return "Staff"


# # Uncomment to load course in all departments
# catalog_page = requests.get('http://rabi.phys.virginia.edu/mySIS/CS2/')
# tree = html.fromstring(catalog_page.content)
#
# catalog = tree.xpath('//td/a/@href')
#
# for item in catalog:
#     print(item)
#     # parse_course(item)

# load course in CS departments only
parse_course('page.php?Semester=1172&Type=Group&Group=CompSci')

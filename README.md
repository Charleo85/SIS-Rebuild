CS4501 SIS Rebuild Project
=====
This project attempts to integrate the current functionality of [UVa SIS](https://sisuva.admin.virginia.edu), [Lou's list](http://rabi.phys.virginia.edu/mySIS/CS2/) and [the Course Forum](http://www.thecourseforum.com), in order to provide students and faculties an efficient way to do academic planning.

Setup
-----
For initial setup, please refer to [Project1](https://github.com/thomaspinckney3/cs4501/blob/master/Project1.md). The next parts assume you have Django/Docker correctly installed, and a mysql container (with credentials given in project 1) up and running.

**If you are grading this project, please follow the instructions below:**

- Pull down the current project for Django:
```bash
$ cd cs4501/app/
$ git clone https://github.com/Charleo85/SIS-Rebuild
```

- Locate and run the docker-compose file:
```bash
$ cd SIS-Rebuild/
$ docker-compose up -d
```

- Verify that the website is working (you should see a helloworld page):
```bash
$ curl 127.0.0.1:8001
```

- We also have a working webpage on a DigitalOcean droplet.

	- visit project server homepage at: [162.243.117.39:8001](http://162.243.117.39:8001)
	- visit admin site: [162.243.117.39:8001/admin](http://162.243.117.39:8001/admin/)
	- login to admin: user = 'root', pw = '135246789'


Project 2
---------

**If you are grading this project, please read this section for our project 2 models and features:**

*****

#### Django Models


- `class Course(models.Model)`

	- required fields (example):

		- `id` (17894) -- *primary, unique, IntegerField*
		- `mnemonic` ("CS")
		- `number` ("4501")
		- `instructor` ("tp3ks") -- *should be an existing instructor id*
		- `max_students` (50) -- *IntegerField*

	- optional fields (example):

		- `section` ("004")
		- `title` ("Internet Scale Application")
		- `meet_time` ("TuTh 3:30 - 4:45pm")
		- `website` ("https://github.com/thomaspinckney3")
		- `location` ("Olsson Hall 120")
		- `description` ("Use Django and Docker to build ...")

- `class Student(models.Model)`

	- required fields (example):

		- `id` ("tq7bw") -- *primary, unique*
		- `first_name` ("Tong")
		- `last_name` ("Qiu")

	- optional fields:

		- `taking_courses` -- *ManyToManyField, through* `Enrollment`

- `class Instructor(models.Model)`

	- required fields (example):

		- `id` ("tp3ks") -- *primary, unique*
		- `first_name` ("Thomas")
		- `last_name` ("Pinckney")

- `class Enrollment(models.Model)`

	- required fields (example):

		- `student` ("tq7bw") -- *should be an existing student id*
		- `course` (17894) -- *should be an existing course id*
		- `enroll_status` ("E" = enrolled, "W" = waitlisted, "D" = dropped, "P" = planned)

*****

#### APIs -- GET and POST requests


- GET requests:

	- To send a GET request, use url "/{{ model_name_lower_case }}/{{ instance_id }}/"
	- Correct requests get back json results with model info
	- Incorrect ones get back a json with "ok" = false
	- Example: To query about instructor with id "tp3ks":

	```bash
	$ curl 127.0.0.1:8001/instructor/tp3ks/
	{
		"ok": true,
		"instructor": {
			"id": "tp3ks",
			"last_name": "Pinckney",
			"first_name": "Tom"
		}
	}
	```
- POST requests:

	- Updating an existing instance:

		- Use the same url as GET to reach for that instance
		- The "id" field in the POST data must match the id in the url
		- All required fields must be filled out
		- If all requirements are satisfied, a json is returned with updated instance info
		- If one or more requirements fail, a json is returned with "ok" = false

	- Creating a new instance:

		- Use url "/{{ model_name_lower_case }}/create/"
		- The "id" must not match an existing instance
		- All required fields must be filled out
		- If all requirements are satisfied, a json is returned with the new instance info
		- If one or more requirements fail, a json is returned with "ok" = false

	- **All POST requests should use form-encoded data**
        
    - Currently, `id` for instructors and students only support uva computing id format, i.e. ab(c)3d(e)


Update Timeline
---------------

- August 30th Project Setup
	- repository init
	- cloud container configured ([Digital Ocean](https://www.digitalocean.com/))
	- project 1 (helloworld) finished

- September 6th
	- new files: models.py, views.py
	- handle HTTP GET request for project 2

- September 10th
	- new files: templates/ dir, forms.py
	- handle HTTP POST request

- September 19th
	- rearrange code layouts
	- docker-compose file created and tested
	- Django models/API finalized for project 2

Contact Us
----------

- Current Collaborators

	- Charlie Wu ([jw7jb@virginia.edu](mailto:jw7jb@virginia.edu))
	- Tong Qiu ([tq7bw@virginia.edu](mailto:tq7bw@virginia.edu))
	- Zakey Faieq ([zaf2xk@virginia.edu](mailto:zaf2xk@virginia.edu))

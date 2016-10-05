CS4501 SIS Rebuild Project
=====
This project attempts to integrate the current functionality of [UVa SIS](https://sisuva.admin.virginia.edu), [Lou's list](http://rabi.phys.virginia.edu/mySIS/CS2/) and [the Course Forum](http://www.thecourseforum.com), in order to provide students and faculties an efficient way to do academic planning.


Setup
-----
For initial setup, please refer to [Project1](https://github.com/thomaspinckney3/cs4501/blob/master/Project1.md). The next parts assume you have Django/Docker correctly installed, and a mysql container (with credentials given in project 1) up and running.

**If you are grading this project, please follow the instructions below:**

- Pull down the current project for Django:
```bash
$ cd ~/cs4501/app/
$ git clone https://github.com/Charleo85/SIS-Rebuild
```

- Locate and run the docker-compose file:
```bash
$ cd SIS-Rebuild/
$ docker-compose up -d
```

- Verify that the website is working (you should see html codes for the homepage):
```bash
$ curl 127.0.0.1:8000
```

- We also have a working webpage on a DigitalOcean droplet. Visit homepage at: [162.243.117.39:8000](http://162.243.117.39:8000)


Project 3
---------

**If you are grading this project, please read this section for our project 3 features:**

********

#### Web Pages

- Home page (`127.0.0.1:8000`):
	- Page design based on Bootstrap CSS Library
	- The central "start" button takes you to the course listing page
	- When you scroll down the page, a "popular courses" section would display the 3 most popular courses
	- The side bar and bottom bar contains links to item listing pages and external pages

- Item listing pages (`/{{ model_name_lower_case}}/`):
	- The title section would display the model name of the item being listed
	- The body section would show all items in this category, in alphabetical order
	- Each listing contains the link to its item detail page

- Item detail pages (`/{{ model_name_lower_case }}/{{ object_id }}/`):
	- The title section would display the course mnemonic and number or instructor name
	- The body section would show all non-blank information about this course/instructor

- The "about" page (`/about/`):
	- This is a brief introduction to the purpose of building our website
	- Contains map / contact info about all contributors to this project

- Thoughts on front-end design:
	- The "most popular" courses is determined by number of students enrolled in each course
	- The item listing for students/enrollments are hidden since these info should be kept private
	- However, you may still view detail of a student(enrollment) at `/student(enrollment)/{{ object_id }}/`

********

#### Container Architecture

- Models api: please refer to the (updated) documentation for project 2.

- Experience api: sends GET requests to models api, processes the retrieved json data, and returns them back to the web layer.

- Web layer: sends GET requests to experience api, and sends data to Django templates for rendering.

- Please see our `views.py` in each layer for a detailed reference.

********

#### User stories and Unit testings

To be added...


Project 2
---------

#### Django Models

- `class Course(models.Model)`

	- required fields (example):

		- `id` ("17894") -- *primary, unique*
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

	- To send a GET request, use url "/api/{{ model_name_lower_case }}/detail/{{ instance_id }}/"
	- use url "/api/{{ model_name_lower_case }}/all/" to retrieve all models
	- Correct requests get back json results with model info
	- Incorrect ones get back a json with "ok" = false
	- Example: To query about instructor with id "tp3ks":

	```bash
	$ curl 127.0.0.1:8001/api/instructor/detail/tp3ks/
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

		- Use the same url as GET to reach for a particular instance
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

- Fixtures:

    - Course: 5 models, list of `id`: `10835`, `16976`, `17894`, `19078`, `19417`.
    - Instructor: 4 models, list of `id`: `asb2t`, `dee2b`, `mve2x`, `tp3ks`.
    - Student: 3 models, list of `id`: `jw7jb`, `tq7bw`, `zaf2xk`.
    - Enrollment: 6 models: students `jw7jb`, `tq7bw`, `zaf2xk` in course `17894`; students `jw7jb`, `tq7bw` in course `19078`; student `jw7jb` in course `16974` (`enroll_status = W`).


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

- September 28th
	- web and experience layers initialized
	- document structure change
	- docker-compose file support 3 containers
	- User stories created

- September 30th
	- Models layer api's optimized
	- First draft of experience layer service
	- Webpage templates and stylesheets created

- October 5th
	- Unit tests created and tested
	- Exp and web layers finalized for project 3


Contact Us
----------

- Current Collaborators

	- Charlie Wu ([jw7jb@virginia.edu](mailto:jw7jb@virginia.edu))
	- Tong Qiu ([tq7bw@virginia.edu](mailto:tq7bw@virginia.edu))
	- Zakey Faieq ([zaf2xk@virginia.edu](mailto:zaf2xk@virginia.edu))

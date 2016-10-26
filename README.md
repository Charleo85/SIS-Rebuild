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

- We also have a working webpage on a DigitalOcean droplet. Visit homepage at: [162.243.117.39:8000](http://162.243.117.39:8000).


Project 4
---------

**If you are grading this project, please read this section for our project 4 features.**

*********

#### Login and User Authentication

- Login page:
	- Please use our side bar on the right of the webpage to visit our login page.
	- Two types of users: students and instructors. Default login page is for students (`/student/login/`); use the "Not a student" link to navigate to instructor login page (`/instructor/login/`).
	- If the login succeeds, you would be redirected to the page you specified with `?next=/your/link`. If you did not specify a `next`, you would be redirected to your own profile page.
	- If the login fails, corresponding error message would be displayed on the page.

- Profile page:
	- Displays all relevant info about the current user (including username, which is not visible if not logged in).
	- Includes a link to logout current user. If you are an instructor, the page also includes a link for creating courses.
	- If you are logged in, the "login" link on the side bar would be automatically changed to a "profile" link that directs you to your profile page.

- Several pre-determined user credentials (in fixture):
	- instructors: `id = tp3ks, username = tp3ks, password = thomas`; `id = asb2t, username = asb2t, password = creepy`; `id = dee2b, username = dee2b, password = daveevans`; `id = mve2x, username = mve2x, password = ershov`.
	- Students: `id = tq7bw, username = tq7bw, password = tonyqiu`; `id = jw7jb, username = jw7jb, password = charlie`; `id = zaf2xk, username = zaf2xk, password = zakeyfaieq`.

#### Sign Up and Create User

- Sign up page:
	- Please first visit our login page, and then click the "sign up" link to visit our sign up page.
	- Sign up supports two types of users as well. To sign up as a specific type of user, use the url `/{{ modelname}}/signup/`.
	- Complete all three steps on the sign up page to sign up a new user. **Note:** you need to use a good password that is: 1) at least 6 digits, 2) not involving only numbers.
	- If the sign up succeeds, you would be directed to a "congratulations" info page. If it fails, correct error message would be displayed.

#### Create Listing (Course):

- The create listing page (`/course/create/`):
	- Only users of the type "instructor" has permission to create a new course. As noted before, you can visit the create course page via the link on your profile page, if you are an instructor.
	- The required fields on the create course page are: `mnemonic`, `number`, `course id`, `instructor id`, and `student capacity`.
	- If the creation is successful, you would be redirected to the detail page of the course you've just signed up. If not, correct error messages would be displayed.



Project 3
---------

#### User stories and Unit testing

- User Stories:

	1. As a Student, I want to create or update my own profile.
	2. As a Student, I want to modify my course enrollment.
	3. As an Instructor, I want to create or update course profile.
	4. As a Administrator, I want to modify student's course enrollment.
	5. As a General User, I want to access course profile.

- Unit testing (See [`tests.py`](models/api/tests.py) for details):

	- Story i:
		- A student named "Scott Gilb" with id `sg4fc` is created and verified.
		- His name (profile) is then changed to "scotty gilb" and verified again.

	- Story ii:
		- The enroll status of student `tq7bw` in course `17894` is changed to "waitlisted" and verified.
		- A new enrollment to enroll student `tq7bw` in course `16976` is created and verified.

	- Story iii:
		- A new course `17615` with title `Capstone Practicum` is created and verified.
		- The course title and its max student capacity was modified and verified again.

	- Story iv:
		- The enrollment of student `jw7jb` in course `16976` is deleted and verified.

	- Story v:
		- The lookup of course mnemonic `MATH` and number `5653` returns the result as expected.

********

#### Web Pages

- Home page (`127.0.0.1:8000`):
	- Page design based on Bootstrap CSS Library.
	- The central "start" button takes you to the course listing page.
	- When you scroll down the page, a "popular courses" section would display the 3 most popular courses.
	- The side bar and bottom bar contains links to item listing pages and external pages.

- Item listing pages (`/{{ model_name_lower_case}}/`):
	- The title section would display the model name of the item being listed.
	- The body section would show all items in this category, in alphabetical order.
	- Each listing contains the link to its item detail page.

- Item detail pages (`/{{ model_name_lower_case }}/{{ object_id }}/`):
	- The title section would display the course mnemonic and number or instructor name.
	- The body section would show all non-blank information about this course/instructor.

- The "about" page (`/about/`):
	- This is a brief introduction to the purpose of building our website.
	- Contains map / contact info about all contributors to this project.

- Thoughts on front-end design:
	- The "most popular" courses is determined by number of students enrolled in each course.
	- The item listing for students/enrollments are hidden since these info should be kept private.
	- However, you may still view detail of a student(enrollment) at `/student(enrollment)/{{ object_id }}/`.

********

#### Container Architecture

- Models api: please refer to the (updated) documentation for project 2.

- Experience api: sends GET requests to models api, processes the retrieved json data (by using Python dictionaries), and returns data back to the web layer.

- Web layer: sends GET requests to experience api, and sends data to Django templates for rendering.

- Please see our `views.py` in each layer for a detailed reference.


Project 2
---------

#### Django Models

- `class Course(models.Model)`

	- required fields (example):

		- `id` ("17894") -- *primary, unique, format = `\d+`*
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

		- `id` ("tq7bw") -- *primary, unique, format = `[a-zA-Z0-9]+`*
		- `first_name` ("Tong")
		- `last_name` ("Qiu")
		- `username` ("tq7bw")
		- `password` ("tonyqiu")

	- optional fields:

		- `taking_courses` -- *ManyToManyField, through* `Enrollment`

- `class Instructor(models.Model)`

	- required fields (example):

		- `id` ("tp3ks") -- *primary, unique, format = `[a-zA-Z0-9]+`*
		- `first_name` ("Thomas")
		- `last_name` ("Pinckney")
		- `username` ("tp3ks")
		- `password` ("thomas")

- `class Enrollment(models.Model)`

	- required fields (example):

		- `student` ("tq7bw") -- *should be an existing student id*
		- `course` (17894) -- *should be an existing course id*
		- `enroll_status` ("E" = enrolled, "W" = waitlisted, "D" = dropped, "P" = planned)

*****

#### APIs -- GET and POST requests

- GET requests:

	- To send a GET request, use url "/api/{{ model_name_lower_case }}/detail/{{ instance_id }}/".
	- use url "/api/{{ model_name_lower_case }}/all/" to retrieve all models.
	- Correct requests get back json results with model info and `status_code = 200` (ok).
	- Incorrect ones get back a json with `status_code` = some error code (eg. `404`).
	- Example: To query about instructor with id "tp3ks":

	```bash
	$ curl 127.0.0.1:8001/api/instructor/detail/tp3ks/
	{
		"status_code": 200,
		"instructor": {
			"id": "tp3ks",
			"last_name": "Pinckney",
			"first_name": "Tom"
		}
	}
	```

- POST requests:

	- Updating an existing instance:

		- Use the same url as GET to reach for a particular instance.
		- The "id" field in the POST data must match the id in the url.
		- All required fields must be filled out.
		- If all requirements are satisfied, a json is returned with updated info and `status_code = 201`.
		- If one or more requirements fail, a json is returned with `status_code = 400` (bad request).

	- Creating a new instance:

		- Use url "/{{ model_name_lower_case }}/create/".
		- The "id" must not match an existing instance.
		- All required fields must be filled out.
		- If all requirements are satisfied, a json is returned with new instance info and `status_code = 202`.
		- If one or more requirements fail, a json is returned with `status_code = 400` (bad request).

	- Deleting an existing instance:

		- Use url "/{{ model_name_lower_case }}/delete/".
		- Only one required field: instance "id", must match some existing instance.
		- **Warning**: when processing a delete request, all related instances would be deleted as well. For example, if you delete an instructor, all courses of this instructor would also be deleted.
		- If the delete is successful, a json is returned with `status_code = 202`.
		- If the delete has failed, a json is returned with `status_code = 400` (bad request).

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
	- User stories written

- September 30th
	- Models layer api improved and tested
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

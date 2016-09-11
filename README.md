CS4501 SIS Rebuild Project
=========
This project attempts to integrate the current functionality of [UVa SIS](https://sisuva.admin.virginia.edu), [Lou's list](http://rabi.phys.virginia.edu/mySIS/CS2/) and [the Course Forum](http://www.thecourseforum.com), in order to provide students and faculties an efficient way to do academic planning.

Django Models
-------------
- Course
	- mnemonic (CS)
	- number (4501)
	- section (005)
	- sis id (17000)
	- instructor (Thomas Pinckney, via instructor model)
	- title (Internet Scale Application)
	- meet time (TuTh 2:00-3:15pm)
	- website (https://github.com/thomaspinckney3/...)
	- location (Olsson Hall 120)
	- description (Use Django and Docker to ...)
	- enrolled students (tracked via enrollment model)
- Student
	- profile (abstract model)
		- first name (Tong)
		- last name (Qiu)
		- computing id (tq7bw)
	- courses (tracked via enrollment model)
- Instructor
	- profile (abstract model)
		- first name (Thomas)
		- last name (Pinckney)
		- computing id (tp3ks)
- Enrollment (Django ManyToManyField)
	- student model
	- course model
	- status (enrolled/waitlist/planned/dropped)

Setup
-----
- For initial setup, refer to [Project1](https://github.com/thomaspinckney3/cs4501/blob/master/Project1.md)
- Pull down the current project for Django:

```bash
$ cd cs4501/app
$ git clone https://github.com/Charleo85/SIS-Rebuild
```

- Cloud Server Credentials
	- visit project server homepage at: [162.243.117.39:8001](http://162.243.117.39:8001)
	- visit admin site: [162.243.117.39:8001/admin](http://162.243.117.39:8001/admin/)
	- login to admin: user = 'admin', pw = '135246789'


Update Timeline
---------------

- August 30th Project Setup
	- repository init
	- cloud container configured ([Digital Ocean](https://www.digitalocean.com/))
	- project 1 (helloworld) finished
- September 6th Project 2 (Models/API)
	- new files: models.py, views.py
	- handle HTTP GET request
- September 10th Project 2
	- new files: templates/ dir, forms.py
	- handle HTTP POST request

Contact Us
----------

- Current Collaborators
	- Charlie Wu [jw7jb@virginia.edu](mailto:jw7jb@virginia.edu)
	- Tong Qiu [tq7bw@virginia.edu](mailto:tq7bw@virginia.edu)
	- Zakey Faieq [zaf2xk@virginia.edu](mailto:zaf2xk@virginia.edu)
- You are very welcome to join us!!!

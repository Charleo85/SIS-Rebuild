CS4501 SIS Rebuild Project
=========
This project attempts to integrate the current functionality of [UVa SIS](https://sisuva.admin.virginia.edu), [Lou's list](http://rabi.phys.virginia.edu/mySIS/CS2/) and [the Course Forum](http://www.thecourseforum.com), in order to provide students and faculties an efficient way to do academic planning.

Models.py
---------
- course
	- mnemonic (math)
	- course number (5653)
	- section id (001)
	- course id (17000)
	- instructor (m. ershov)
	- title (number theory)
	- time (tuth 2:00-3:15pm)
	- location (chem305)
	- description (this is a class...)
	- enrollment ([student1, student2, ...])

- student
	- profile
		- name
		- computing id
	- courses
		- planned
		- enrolled
		- waitlisted

- instructor
	- profile
		- name
		- computing id
	- teaching courses

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


Contact Us
===================

- Current Collaborators

	- Charlie Wu [jw7jb@virginia.edu](mailto:jw7jb@virginia.edu)
	- Tong Qiu [tq7bw@virginia.edu](mailto:tq7bw@virginia.edu)

- You are very welcome to join us!!!
![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)](/license.txt)
![PyPI](https://img.shields.io/pypi/status/Django.svg)
<a href="https://travis-ci.com"><img src="https://travis-ci.com/Charleo85/SIS-Rebuild.svg?token=p3baya2L6nJfueKHztqt&branch=master"></a>
[![Website](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://162.243.117.39)


Grades at UVa
=====
This project attempts to integrate and improve on the current functionality of [Lou's list](http://rabi.phys.virginia.edu/mySIS/CS2/) and [the Course Forum](http://www.thecourseforum.com) by adding improved data visualization of grade distribution data (retrieved through [FOIA](https://en.wikipedia.org/wiki/Freedom_of_Information_Act_(United_States))) in order to provide students and faculty an improved perspective that will aid in the course selection process.
	
You may contribute your thoughts on this project to our [Trello](https://trello.com/b/XTuoK510/isa-project) page.
The models API is documented on [Swagger](https://app.swaggerhub.com/api/charlie/SIS-R/1.0.0).

All [CS 4501 (Internet Scale Application)](https://github.com/thomaspinckney3/cs4501/blob/master/README.md) course related files can be found in the `misc/` directory. Please see [cs4501.md](misc/cs4501.md) for details.

We have a working webpage on DigitalOcean: Visit homepage at: [http://162.243.117.39](http://162.243.117.39).


Setup
--------
For initial setup, please refer to [Project1 @CS4501](https://github.com/thomaspinckney3/cs4501/blob/master/Project1.md). The next parts assume you have Django/Docker correctly installed, and a mysql container (with credentials given in the project) up and running.

- First `clone` or `pull` the current project from Github:
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
$ curl 127.0.0.1
```

- Depending on situations, you might want to reset the MySQL database to its initial state:
```bash
$ docker start mysql
$ chmod 755 misc/scripts/cleardb.sh && ./misc/scripts/cleardb.sh
```


APIv2 Documentation
--------
#### Models (`models/apiv2/models.py`)

**Note: every model begins with a line describing its "required" fields; all other fields can be left blank.

- `Grade`
	- **required:** `num_a`, `num_b`, `num_c`, `num_d`, `num_f`;
	- `average_gpa`: `DecimalField` w/ 3 decimal places;
	- `num_a_plus`, `num_a`, `num_a_minus`, etc. (down to `num_f`): `PositiveSmallIntegerField`;
	- `num_withdraw`, `num_drop`: `PositiveSmallIntegerField`.

- `Course`
	- **required:** `name`, `mnemonic`, `number`, `grade`;
	- `name`, `mnemonic`, `number`: `CharField`;
	- `description`: `TextField`;
	- `grade`: one-to-one relationship with `Grade` model.

- `Section`
	- **required:** `semester`, `section_id`, `sis_id`, `units`, `section_type`, `course`, `instructor`;
	- `semester`, `section_id`, `sis_id`: `CharField`;
	- `units`: `PositiveSmallIntegerField`;
	- `section_type`: `CharField` with choices (lectures, labs, etc.), see `models.py`;
	- `title`, `meeting_time`, `location`: `CharField`;
	- `website`: `URLField`;
	- `capacity`: `PositiveSmallIntegerField`;
	- `description`, `other_info`: `TextField`.
	- `course`: many-to-one relationship with `Course` model;
	- `instructor`: many-to-one relationship with `Instructor` model;
	- `grade`: one-to-one relationship with `Grade` model.

- `User`
	- **required:** `username`, `password`, `name`;
	- `username`, `password`, `name`: `CharField`, `password` field stores hashes;
	- `email`: `EmailField`;
	- `interested_course`: many-to-many relationship with `Section`.

- `Instructor`
	- **required:** `name`, `computing_id`;
	- `name`, `computing_id`: `CharField`;
	- `website`: `URLField`;
	- `email`: `EmailField`;
	- `address`, `cell_phone`: `CharField`;
	- `other_info`: `TextField`;
	- `user`: one-to-one relationship with `User` model (see if the instructor is a registered user).

- `Authenticator` **backend usage only**
	- **required**: `user_id`, `authenticator`, `date_created`;
	- `user_id`, `authenticator`: `CharField`;
	- `date_created`: `DateField` that automatically record dates when an `Authenticator` is created.

#### Views and API URL Rules (`models/apiv2/views.py`)

**Important: The views are written in an object-oriented way, using Django's class-based views. There's a `BaseView` class that defines the basic behaviors of a view (i.e. when it receives a GET, POST, or DELETE request). Every view class extends from this base class, and should define the methods to create/update/lookup a specific model.**

- For model `Course`: base_url = `/apiv2/course`

	- GET
		- use keyword arguments as queries after the base_url.
		- returns an array of objects that matches the given query.
		- example: to retrieve all courses with mnemonic CS and number 2150, use `/apiv2/course?mnemonic=CS&number=2150`.
	
	- POST (create)
		- nothing should be present after the base_url.
		- use key-value pairs as post data (also accepts JSON).
		- returns the id of the newly created object, if successful.
	
	- POST (update)
		- use keyword arguments as queries (same as GET) to filter the single object to update.
		- use key-value pairs as post data (also accepts JSON).
		- each valid key-value pair would correspond to one updated column for the object.
		- returns the id of the updated object, if successful.
	
	- DELETE
		- use keyword arguments as queries (same as GET) to filter the object(s) to delete.
		- no body content should be present for this request.
		- to force deletion of multiple objects, specify `?force=true` in the url query.

Update Timeline
--------

- December 13th, 2016
	- Finished all CS 4501 course projects. Details on [Wiki](https://github.com/Charleo85/SIS-Rebuild/wiki/CS-4501-ISA-Project-Updates).

- January 3rd, 2017
	- Open-source procedures completed; Trello page created.
	- Document structure update.

- January 14th
	- Finished base codes for apiv2 (mostly `models.py` and `views.py`).
	- Tested the new api for model `Course` to make sure it's working.


Contact Us
--------

- Charlie Wu ([jw7jb@virginia.edu](mailto:jw7jb@virginia.edu))
- Tong Qiu ([tq7bw@virginia.edu](mailto:tq7bw@virginia.edu))
- Zakey Faieq ([zaf2xk@virginia.edu](mailto:zaf2xk@virginia.edu))

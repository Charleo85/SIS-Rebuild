![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)](/license.txt)
![PyPI](https://img.shields.io/pypi/status/Django.svg)
<a href="https://travis-ci.com"><img src="https://travis-ci.com/Charleo85/SIS-Rebuild.svg?token=p3baya2L6nJfueKHztqt&branch=master"></a>
[![Website](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://162.243.117.39)


CS4501 SIS Rebuild Project
=====
This project attempts to integrate the current functionality of [UVa SIS](https://sisuva.admin.virginia.edu), [Lou's list](http://rabi.phys.virginia.edu/mySIS/CS2/) and [the Course Forum](http://www.thecourseforum.com), in order to provide students and faculties an efficient way to do academic planning.

You may contribute your thoughts on this project to our [Trello](https://trello.com/b/XTuoK510/isa-project) page.
The models API is documented on [Swagger](https://app.swaggerhub.com/api/charlie/SIS-R/1.0.0).

All [CS 4501 (Internet Scale Application)](https://github.com/thomaspinckney3/cs4501/blob/master/README.md) course related files can be found in the `misc/` directory. Please see [cs4501.md](misc/cs4501.md) for details.


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

- We also have a working webpage on a DigitalOcean droplet. Visit homepage at: [http://162.243.117.39](http://162.243.117.39).


Update Timeline
--------

- December 13th, 2016
	- Finished all CS 4501 course projects. Details on [Wiki](https://github.com/Charleo85/SIS-Rebuild/wiki/CS-4501-ISA-Project-Updates).

- January 3rd, 2017
	- Open-source procedures completed; Trello page created.
	- Document structure update.


Contact Us
--------

- Charlie Wu ([jw7jb@virginia.edu](mailto:jw7jb@virginia.edu))
- Tong Qiu ([tq7bw@virginia.edu](mailto:tq7bw@virginia.edu))
- Zakey Faieq ([zaf2xk@virginia.edu](mailto:zaf2xk@virginia.edu))

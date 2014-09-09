# MUPY

## What is Mupy?

Mupy is a Munin Python Parser. It is written in Python and is powered by Django framework.
Its functionality is pretty straightforward. It parses the HTML DOM of a munin site, stores the graphable
data into a db and provides a friendly user interface for retrieving munin graphs.


### Munin version compatibility
Mupy was built on Munin version 1.4.5, but is supports version 2 as well.


### Installation Requirements
Mupy's installation and operation depends on the following modules/packages

* python-django (>=1.4.5)
* python-mysqldb
* python-ldap (if ldap user auth is needed)
* python-bs4 (won't work with <4)
* memcached


## Installation

1. Untar the package (or clone via git) to your desired location, copy sample_local_settings.py to local_settings.py, apache/django.wsgi.dist to local files ommiting dist and edit loca_settings.py and apache/django.wsgi according to your needs. Pay special attention to:
	- `MUNIN_URL` : url that munin welcome page lives, eg. "http://munin.example.com"
	- `MUNIN_CGI_PATH` : if images are updated frequently (without the need to visit) then set the cgi path here, eg. "cgi-bin/munin-cgi-graph/"

2. To serve via Apache (static files),
create an alias for the static dir in your apache conf and a WSGI script alias eg.

		Alias /static       /<installation_location>/mupy/static
		WSGIScriptAlias /      /<installation_location>/mupy/apache/django.wsgi

3. Run ./manage.py collectstatic
4. Run syncdb and create an admin user. Admin users have permissions to all nodegroups/nodes/graphs
5. Run ./manage.py parse_munin2 to parse the MUNIN_URL and store data into db. In case you have an older version of munin you have to run ./manage parse_munin. A daily cronjob of this command is suggested.
6. Restart Apache (or "touch apache/django.wsgi") and enjoy
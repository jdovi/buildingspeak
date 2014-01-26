.. _getting_started:

***************
Getting Started
***************

To contribute to BuildingSpeak development, the following are required:

* Python 2.7.x (3.x is out, but 2.7 still widely used)
* Postgres
* Django 1.5.1
* git for version control
* various Python modules (detailed below).

There are a variety of ways to install/use Python and Django.  These docs are aimed at Windows users and will cover the use of Python within PythonXY's Spyder tool.  Also note that some of the code is specific to the hosting of BuildingSpeak on Heroku (also covered in more detail later).

Python and Friends
==================
Install the `PythonXY <https://code.google.com/p/pythonxy/wiki/Downloads>`_ distribution.  The easiest way is to download/run the executables.

You might need to adjust your PATH environment variable to include paths to Python executable and additional scripts. For example, if your Python is installed in C:\Python27\, the following paths need to be added to PATH::

	C:\Python27\; C:\Python27\Scripts;

This will make a primary Python installation available on the machine.  Included in the source code for BuildingSpeak is virtual Python environment, which is the actual Python installation that will be used by BuildingSpeak.  But the primary installation is helpful for local development within Spyder, so we will do both, with the result that each package is loaded into both the main local machine environment and the virtual environment.

Although not required for some activities, e.g. making :file:`git commit`s, it's a good general practice to activate the :file:`venv` when doing anything from the command line::

C:\...\BuildingSpeak> venv\scripts\activate.bat
(venv) C:\...\BuildingSpeak>

Once Python is installed, we need to install quite a few packages that perform various functions.  These packages are best managed with a tool called :file:`pip`, which requires another tool called :file:`setuptools`.  Follow `these instructions <http://www.pip-installer.org/en/latest/installing.html>`_ to download :file:`ez_setup.py` and :file:`get-pip.py`.  Then run the following two lines from the command prompt::

	C:\...\BuildingSpeak> python ez_setup.py
	[... output from running ez_setup.py]
	C:\...\BuildingSpeak> python get-pip.py

With :file:`pip` installed, most packages can be installed with the following::

	C:\...\BuildingSpeak> pip install my_package_name

Make sure all of the following packages are installed on the local machine (they should already exist in the :file:`venv` contained in the BuildingSpeak directory.::

	Django==1.5.1
	South==0.8.1
	boto==2.9.9
	croniter==0.3.3
	dj-database-url==0.2.2
	dj-static==0.0.5
	django-model-utils==1.4.0
	django-storages==1.1.8
	django-toolbelt==0.0.1
	djorm-ext-pgarray==0.6
	docutils==0.11
	gunicorn==17.5
	jinja2==2.7.1
	jsonpickle==0.6.1
	markupsafe==0.18
	numpy==1.7.0
	psycopg2==2.4.5
	pygments==1.6
	python-dateutil==2.1
	pytz==2013b
	requests==1.2.0
	scipy==0.11.0
	six==1.3.0
	sphinx==1.2
	static==0.4
	wsgiref==0.1.2
	zope.interface==4.0.5
	pandas==0.12.0
	statsmodels==0.4.3
	redis==2.7.6
	rq==0.3.8
	times==0.6.2
	tropo-webapi-python==0.1.3
	mandrill>=1.0.6
	stripe==1.11.0

.. _launching_new_db_local:

****************************
Launching New Local Instance
****************************
This section details the process for launching a new local version of BuildingSpeak for the purpose of developing and testing code.  It assumes all the steps in the :ref:`getting_started` section have been completed, meaning the local environment has the necessary setup.

Remove Old Stuff
==================
Sometimes phantom connections exist in the database that prevent deletion.  To kill all existing connections, execute the following in the Postgres shell (accessible from the Start menu)::

postgres=# select pg_terminate_backend(pid) from pg_stat_activity where datname='old_local_db_name';

To delete the old database and any migrations, from the command line run the following, inserting the full path to your BuildingSpeak folder in the second line::

(venv) C:\...\BuildingSpeak> dropdb old_local_db_name
(venv) C:\...\BuildingSpeak> rd /s /q C:\...\BuildingSpeak\BuildingSpeakApp\migrations  

Create New Database
===================
To create a new database, run::

(venv) C:\...\BuildingSpeak> createdb buildingspeaklocaldb

Special Prerequisites
======================
The forms in :file:`models_Forms.py` previously had fields that would break the first command to set up the database with South, presumably because these attributes had :file:`choices` fields dependent on model objects that didn't yet exist prior to the first South command to initialize the database schema.  These fields were deemed unnecessary and removed, but future modifications may cause similar issues again.  (The inability to populate :file:`FileField` attributes is a similar issue - the :file:`FileField` upload function requires a model ID which doesn't yet exist during the initial creation of the model instance.)

The solution is simply to comment out any fields dependent on other models prior to the first South command.  Then run the South commands to initialize and migrate.  Afterwards, uncomment the code and migrate the database.  However, note that this should only be an issue on the very first initialization.  For developers receiving the repository, multiple migrations should already exist, and only a :file:`python manage.py migrate BuildingSpeakApp` should be necessary to sync the newly created database with the latest migration.

.. _syncing_with_south
Syncing with South
======================
First we initialize the South migration history with::

(venv) C:\...\BuildingSpeak> python manage.py schemamigration BuildingSpeakApp --initial

This should also offer the setup of a superuser.  Once initialized, we can perform the first migration::

(venv) C:\...\BuildingSpeak> python manage.py migrate BuildingSpeakApp

Now the database is set up with one user and can be accessed via the admin portal once we launch the development server with::

(venv) C:\...\BuildingSpeak> python manage.py runserver

Open a browser and navigate to :file:`127.0.0.1:8000/admin`, where you can log in as the superuser you created during the database setup step.


.. _switching_heroku_local
Switching the Code Between Heroku and Local
============================================
The repository you originally access will be set for Heroku.  Before you can load data into the new database from within Django, you need to switch several settings from Heroku to local.  There are several reasons for this:

* For security, access keys should never be stored in the source code; instead, they are stored as local environment variables.  Because Windows doesn't have a good way to handle these, we need to explicitly define these variables in the code.
* Certain features such as queuing use modules that aren't supported on Windows, causing BuildingSpeak to fail unless the lines calling such modules are removed.
* Other settings such as the name of the database also vary by local environment and need to be defined explicitly.

In BuildingSpeak's :file:`settings.py` file, replace the original :file:`DATABASES` definition (shown commented out here) with something like the sample shown, using the username and password you set up during :ref:`syncing_with_south`.  Also comment out the two :file:`dj_database_url` lines at the bottom of the file.::

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': '',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}
DATABASES = {    
    'default': {        
		'ENGINE': 	'django.db.backends.postgresql_psycopg2',
		'NAME':   	'buildingspeaklocaldb',
		'USER':   	'your_username',
		'PASSWORD': 'your_password',
		'HOST': 	'localhost',
		'PORT': 	'5432',
    }
}
...
#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()

Replace the Mandrill, Stripe, and Amazon access keys with the values provided by management (not stored anywhere in these docs which live with the source code!).  Note some of the keys have different values for staging and production, so make sure you get the right ones - do not write test data to production!  Both sets are shown below, but you would only enter the line once with the appropriate staging or production variable.::

	#AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
	#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') 
	#AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
	AWS_ACCESS_KEY_ID='xxxxxx'
	AWS_SECRET_ACCESS_KEY='xxxxxx'
	local development:
	AWS_STORAGE_BUCKET_NAME='xxxxxx-localdev'
	staging:
	AWS_STORAGE_BUCKET_NAME='xxxxxx-staging'
	production:
	AWS_STORAGE_BUCKET_NAME='xxxxxx-production'

	#MANDRILL_APIKEY = os.environ.get('MANDRILL_APIKEY')
	#MANDRILL_USERNAME = os.environ.get('MANDRILL_USERNAME')
	staging:
	MANDRILL_APIKEY='xxxxxx'
	MANDRILL_USERNAME='appXXXX@heroku.com'
	production:
	MANDRILL_APIKEY='xxxxxx'
	MANDRILL_USERNAME='appXXXX@heroku.com'

	STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
	STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
	staging:
	STRIPE_SECRET_KEY='sk_test_xxxxxx'
	STRIPE_PUBLISHABLE_KEY='pk_test_xxxxxx'
	production:
	STRIPE_SECRET_KEY='sk_live_xxxxxx'
	STRIPE_PUBLISHABLE_KEY='pk_live_xxxxxx'

Comment out the following two lines in :file:`models_WeatherStation.py` and :file:`views.py`::

#from rq import Queue
#from worker import conn

Also in :file:`views.py`, switch the following lines to remove queuing since :file:`RQ` isn't available on Windows::

#q = Queue(connection=conn)
#result = q.enqueue(meter.upload_bill_data)
meter.upload_bill_data()

Finally, add your local address to the :file:`ALLOWED_HOSTS` variable in :file:`settings.py`.  This is required when :file:`DEBUG` is set to False, which is sometimes useful to test administrative emailing features.::

ALLOWED_HOSTS = ['.buildingspeak-staging.herokuapp.com',
                 '.buildingspeak-staging.com',
                 '.buildingspeak-production.herokuapp.com',
                 '.buildingspeak-production.com',
                 '127.0.0.1']

Populating Framework Data
=========================
Django's functionality for creating management commands is useful for streamlining the loading of framework data (utilities, weather data, rate schedules, etc.) and customer data into BuildingSpeak.  See :ref:`management_commands` for details on using this functionality.

Launching the User Interface
============================
Once you have some data, launch the development-only webserver locally with::

(venv) C:\...\BuildingSpeak> python manage.py runserver

Open a browser and navigate to :file:`127.0.0.1:8000/`, where you can log in as the superuser you created during the database setup step.

Additional Notes
================
Now you can develop and test locally.  Remember to switch settings back from local before pushing any code to Heroku or github to avoid storing any access keys in online repositories.
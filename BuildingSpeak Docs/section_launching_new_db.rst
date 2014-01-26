.. _launching_new_db:

***********************
Launching New Instance
***********************
This section details the process for launching a new database.  It covers both local installation and Heroku installation, with local installation covered first as it's required prior to a push to Heroku.  It also assumes all the steps in the :ref:`getting_started` section have been completed, meaning the local environment has the necessary setup.

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

(venv) C:\...\BuildingSpeak> createdb new_local_db_name

Special Prerequisites
======================
The forms in :file:`models_Forms.py` previously had fields that would break the first command to set up the database with South, presumably because these attributes had :file:`choices` fields dependent on model objects that didn't yet exist prior to the first South command to initialize the database schema.  These fields were deemed unnecessary and removed, but future modifications may cause similar issues again.  (The inability to populate :file:`FileField` attributes is a similar issue - the :file:`FileField` upload function requires a model ID which doesn't yet exist during the initial creation of the model instance.)

The solution is simply to comment out any fields dependent on other models prior to the first South command.  Then run the South commands to initialize and migrate.  Afterwards, uncomment the code and migrate the database.  

Syncing with South
======================
First we initialize the South migration history with::

(venv) C:\...\BuildingSpeak> python manage.py schemamigration BuildingSpeakApp --initial

This should also offer the setup of a superuser.  Once initialized, we can perform the first migration::

(venv) C:\...\BuildingSpeak> python manage.py migrate BuildingSpeakApp

Now the database is set up with one user and can be accessed via the admin portal once we launch the development server with::

(venv) C:\...\BuildingSpeak> python manage.py runserver

Open a browser and navigate to :file:`127.0.0.1:8000/admin`, where you can log in as the superuser you created during the database setup step.

Populating Framework Data
=========================
Django's functionality for creating management commands is useful for streamlining the loading of framework data (utilities, weather data, rate schedules, etc.) and customer data into BuildingSpeak.  The folder :file:`C:\\...\\BuildingSpeak\\BuildingSpeakApp\\management\\commands\\` contains files that may be executed with::

(venv) C:\...\BuildingSpeak> python manage.py mgt_command_filename



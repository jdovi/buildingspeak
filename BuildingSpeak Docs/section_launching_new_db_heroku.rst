.. _launching_new_db_heroku:

*****************************
Launching New Heroku Instance
*****************************
This section details the process for launching a new database on Heroku.  It covers deleting and creating databases and setting environment variables needed by BuildingSpeak.

Remove Old Stuff
==================
Delete an existing database with::

(venv) C:\...\BuildingSpeak> heroku pg:reset DATABASE

Create New Database
===================
Create a new database via heroku.com or::

(venv) C:\...\BuildingSpeak> heroku addons:add heroku-postgresql

Then make it the primary database for the application with::

(venv) C:\...\BuildingSpeak> heroku pg:promote HEROKU_POSTGRESQL_<new-database-color>

Special Prerequisites
======================
The forms in :file:`models_Forms.py` previously had fields that would break the first command to set up the database with South, presumably because these attributes had :file:`choices` fields dependent on model objects that didn't yet exist prior to the first South command to initialize the database schema.  These fields were deemed unnecessary and removed, but future modifications may cause similar issues again.  (The inability to populate :file:`FileField` attributes is a similar issue - the :file:`FileField` upload function requires a model ID which doesn't yet exist during the initial creation of the model instance.)

The solution is simply to comment out any fields dependent on other models prior to the first South command.  Then run the South commands to initialize and migrate.  Afterwards, uncomment the code and migrate the database.  However, note that this should only be an issue on the very first initialization.  For developers receiving the repository, multiple migrations should already exist, and only a :file:`python manage.py migrate BuildingSpeakApp` should be necessary to sync the newly created database with the latest migration.

.. _syncing_with_south
Syncing with South
======================
Even though migrations already exist in the repository, we first have to run the following to create tables (specifically the :file:`south_migrationhistory` table) and the first superuser::

(venv) C:\...\BuildingSpeak> heroku run python manage.py syncdb

Then migrate with::

(venv) C:\...\BuildingSpeak> heroku run python manage.py migrate BuildingSpeakApp

You should now be able to access the admin with the new user you created, although no models exist except the new :file:`User` (no :file:`UserProfile` yet).


Switching the Code Between Local & Heroku
=========================================
The repository you originally access will be set for Heroku.  See :ref:`switching_heroku_local` for instructions to set settings for local development.

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
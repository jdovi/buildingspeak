.. _management_commands:

*****************************
Using Management Commands
*****************************

Populating Framework Data
=========================
Django's functionality for creating management commands is useful for streamlining the loading of framework data (utilities, weather data, rate schedules, etc.) and customer data into BuildingSpeak.  The folder :file:`C:\\...\\BuildingSpeak\\BuildingSpeakApp\\management\\commands\\` contains files that may be executed with::

(venv) C:\...\BuildingSpeak> python manage.py mgt_command_filename

The same approach can be used on Heroku with :file:`heroku run python manage.py mgt_command_filename`.

Automated uploading of files is achieved via the :file:`C:\\...\\BuildingSpeak\\BuildingSpeak\\static\temporary_files\\` folder.  Place files such as images and meter bill data into this folder, and correctly reference them in a management command module.  The folder will initially be uploaded to S3 during the push to Heroku.  The management command will then be able to access the file from this folder and save it in the appropriate place on S3.  For example, an Account image file will first be read from the :file:`temporary_files` folder but then be stored under the Account folder on S3 once your management command saves the image file to the Account model.

The supporting (non-customer) data in BuildingSpeak is loaded in using :file:`BuildingSpeakBuiltins_XXX.py`, where XXX is a sequential, 3-digit numbering system to enable continuous management of the built-in models and their data.  For example, :file:`BuildingSpeakBuiltins_001.py` contains the :file:`WeatherStation` :file:`ATL - downtown west`, the :file:`Utility` :file:`Georgia Power Company`, etc.  As new built-ins are needed, additional :file:`BuildingSpeakBuiltins_XXX.py` files can be created, and all built-ins can be recreated by simply running this series of management commands in sequential order.

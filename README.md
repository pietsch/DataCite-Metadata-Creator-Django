DataCite-Metadata-Creator-Django
================================

Note that this is an unfinished prototype that may never be completed.
It may still be useful creating the metadata XML file required for registering a data DOI with DataCite <http://datacite.org>.
This tool does not send any data to DataCite.


Requirements
------------

- django 1.5
- sqlite3


Setup
-----

cd datadoi
## Now generate a SECRET_KEY at http://www.miniwebtool.com/django-secret-key-generator/ or elsewhere and change it in `datadoi/settings.py`.
./manage.py syncdb     ## This will ask you to set a name and password for an admin user. You will need these credentials later on!
./manage.py runserver  ## Or, if this Django app should be accessible to everyone on your network, say ./manage.py runserver 0.0.0.0:8000


Usage
-----

- Open http://0.0.0.0:8000/ in a web browser.
- Click “Register a new dataset” and enter the credentials you set in the syncdb step.
- Click the “+ Add” beside “Resources: Enter new datasets here”.
- Fill in the forms, and click “Save”!
- To download or preview the XML you generated, visit http://0.0.0.0:8000/queue/


* * * * *
*Christian Pietsch*

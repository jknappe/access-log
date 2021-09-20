# Research green roof access log

This Flask app serves as an Access Log for the UFZ research green roof. It runs a virtual server on a Raspberry Pi 400 with mouse and touchscreen display serving a data collection form to record name, affiliation and timestamp of people getting on and off the roof. The database can be exported to CSV in admin mode.

## Dongles

A total of 10 dongles are registered with the app. The IDs of the 10 valid dongles are hard-coded into the `app.py` file. Each dongle, when scanned, submits a 10-digit ID followed by a line break that triggers submission of the HTMl form into the database. If a non-valid dongle is scanned, an error message will occur and the app will redirect to the index page.

## Admin mode

To enter admin mode type 'admin' + RETURN on the index page.

I admin mode you can see a list of the 25 most recent records in the database and you can alos export the entire database to CSV. The resulting file will be stored in the browser's default download folder, i.e. "Downloads" in most cases.

## Coding specs

### Recreating the database

The database 'access-log.db' is stored in the app's home folder. If this file is deleted, the entire database is lost. Please export the database to CSV as described above and copy these files to another computer for permanent storage.

In case a new database needs to be created, navigate to the app folder and run python3 in the command line. Then run the following commands:

```
from app import db
db.create_all()
```




#!/bin/sh
# launcher.sh
# navigate to home directory, then to app directory, then start the app, then return back to home directory

cd /
cd home/pi/access-log
python3 app.py
cd /

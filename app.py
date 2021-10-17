from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import flask_excel as excel
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///access-log.db'
app.secret_key = 'fgd2L"))+=23F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class access_log_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    affiliation = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id %r>' % self.id

@app.route('/ascend_form', methods=['POST', 'GET'])
def ascend_form():
    error = False
    errorDE = None
    errorEN = None
    valid_tokens = ['t', '0001101747' , '0001964054', '0014488389', '0014405751', '0004033874', '0014580266', '0001951950', '0007000492', '0014502443', '0014552070']

    if request.method == 'POST':
        token = request.form['token']
        action = request.form['action']
        name = request.form['name']
        affiliation = request.form['affiliation']
    
        if token in valid_tokens:
            new_entry = access_log_DB(token = token, action = action, name = name, affiliation = affiliation)

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/ascend_success')
            except:
                return 'Could not write to data base.'

        else:
            error = True
            errorDE = 'Dieser Dongle kann nicht gelesen werden. Bitte einen der gültigen Dongles scannen.'
            errorEN = 'This dongle cannot be read, please scan one of provided dongles.'
            return render_template('/invalid.html', error = error, errorDE = errorDE, errorEN = errorEN)

    else:
        # read swipes data from the database
        swipes = access_log_DB.query.order_by(access_log_DB.datetime.desc()).all()
        # render the index pages with swipes data available
        return render_template('ascend_form.html', swipes=swipes)

@app.route('/descend_form', methods=['POST', 'GET'])
def descend_form():
    error = False
    errorDE = None
    errorEN = None
    valid_tokens = ['t', '0001101747' , '0001964054', '0014488389', '0014405751', '0004033874', '0014580266', '0001951950', '0007000492', '0014502443', '0014552070', '0011248286', '0011248301', '0011250890', '0003912831', '0003858707', '0015466677', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087']

    if request.method == 'POST':
        token = request.form['token']
        action = request.form['action']
        name = request.form['name']
        affiliation = request.form['affiliation']
    
        if token in valid_tokens:
            new_entry = access_log_DB(token = token, action = action, name = name, affiliation = affiliation)

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/descend_success')
            except:
                return 'Could not write to data base.'

        else:
            error = True
            errorDE = 'Dieser Dongle kann nicht gelesen werden. Bitte einen der gültigen Dongles scannen.'
            errorEN = 'This dongle cannot be read, please scan one of provided dongles.'
            return render_template('/invalid.html', error = error, errorDE = errorDE, errorEN = errorEN)

    else:
        # render descend_form page
        return render_template('descend_form.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    data = access_log_DB.query.order_by(access_log_DB.datetime.desc()).all()   
    return render_template('admin.html', data=data)

    

@app.route('/show_data', methods=['POST', 'GET'])
def show_data():
    data = access_log_DB.query.order_by(access_log_DB.datetime.desc()).all()   
    return render_template('show_data.html', data=data)



@app.route('/download', methods=['GET'])
def download_data():
    id = access_log_DB.query.with_entities(access_log_DB.id).order_by(access_log_DB.datetime.desc()).all()
    datetime = access_log_DB.query.with_entities(access_log_DB.datetime).order_by(access_log_DB.datetime.desc()).all()
    token = str(access_log_DB.query.with_entities(access_log_DB.token).order_by(access_log_DB.datetime.desc()).all())
    name = access_log_DB.query.with_entities(access_log_DB.name).order_by(access_log_DB.datetime.desc()).all()
    affiliation = access_log_DB.query.with_entities(access_log_DB.affiliation).order_by(access_log_DB.datetime.desc()).all()
    action = access_log_DB.query.with_entities(access_log_DB.action).order_by(access_log_DB.datetime.desc()).all()
    excel.init_excel(app)
    extension_type = "csv"
    filename = "access_log_export" + "." + extension_type
    d = {'action': action, 'affiliation': affiliation, 'name': name, 'token': token, 'datetime': datetime, 'id': id}
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)




    
@app.route('/')
def index():
    if request.method == 'POST':
        token = request.form['token']
        if token == 'admin':
            return render_template('admin.html')
    return render_template('index.html')

@app.route('/ascend_success')
def ascend_success():
    return render_template('ascend_success.html')

@app.route('/descend_success')
def descend_success():
    return render_template('descend_success.html')







@app.route('/shutdown')
def shutdown():
    os.system("sudo shutdown -h now")


if __name__ == "__main__":
     app.run(debug=True)


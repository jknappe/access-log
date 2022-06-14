from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

import flask_excel as excel
import pandas as pd
import os, shutil, glob, time

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'fgd-accesslog@outlook.com'
app.config['MAIL_PASSWORD'] = 'test'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)


# Set up SQL database
#=====================================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///access-log.db'
app.secret_key = 'fgd2L"))+=23F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class access_log_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    affiliation = db.Column(db.String(100), nullable=False)    
    work_inspection = db.Column(db.String(10), default=False, nullable=False)
    work_maintenance = db.Column(db.String(10), default=False, nullable=False)
    work_equipment = db.Column(db.String(10), default=False, nullable=False)
    work_sampling = db.Column(db.String(10), default=False, nullable=False)
    work_measurements = db.Column(db.String(10), default=False, nullable=False)
    work_drone = db.Column(db.String(10), default=False, nullable=False)
    work_tour = db.Column(db.String(10), default=False, nullable=False)
    work_other = db.Column(db.String(10), default=False, nullable=False)
    work_other_text = db.Column(db.String(100), nullable=False) 
    nr_people = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id %r>' % self.id

# Set up rendered pages and functions
#=====================================================  

@app.route('/', methods=['POST', 'GET'])
def index():
    admin_tokens = ['admin', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087', '0015466677']

    if request.method == 'POST':
        scanned_token = request.form['token']

        if scanned_token in admin_tokens:
            # if scanned_token == 'admin':
            #     name = 'Admin'
            # elif scanned_token == '0015465087':
            #     name = 'Jan'
            # elif scanned_token == '0004498655':
            #     name = 'Lucie'
            # elif scanned_token == '0015465203':
            #     name = 'Katy'
            # elif scanned_token == '0004656070':
            #     name = 'Max'
            # elif scanned_token == '0003949645':
            #     name = 'Ralf'
            # elif scanned_token == '0004484801':
            #     name = 'Niels'
            # elif scanned_token == '0015466677':
            #     name = 'Christian'
            # elif scanned_token == '0004724076':
            #     name = 'Peter'
            # elif scanned_token == '0004499470':
            #     name = 'Admin 9'
            # elif scanned_token == '0015465255':
            #     name = 'Admin 10'            
            return render_template('admin_index.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/login_form', methods=['POST', 'GET'])
def login_form():
    error = False
    errorDE = None
    errorEN = None
    valid_tokens = ['t', '0001101747' , '0001964054', '0014488389', '0014405751', '0004033874', '0014580266', '0001951950', '0007000492', '0014502443', '0014552070', '0011248286', '0011248301', '0011250890', '0003912831', '0003858707', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087', '0015466677']

    if request.method == 'POST':
        token = request.form['token']
        action = request.form['action']
        name = request.form['name']
        affiliation = request.form['affiliation'] 
        nr_people = request.form['nr_people'] 
        if request.form.get('work_inspection'):   
            work_inspection = request.form['work_inspection']
        else:
            work_inspection = "0"
        if request.form.get('work_maintenance'):   
            work_maintenance = request.form['work_maintenance']
        else:
            work_maintenance = "0"
        if request.form.get('work_equipment'):   
            work_equipment = request.form['work_equipment']
        else:
            work_equipment = "0"
        if request.form.get('work_sampling'):   
            work_sampling = request.form['work_sampling']
        else:
            work_sampling = "0"
        if request.form.get('work_measurements'):   
            work_measurements = request.form['work_measurements']
        else:
            work_measurements = "0"
        if request.form.get('work_drone'):   
            work_drone = request.form['work_drone']
        else:
            work_drone = "0"
        if request.form.get('work_tour'):   
            work_tour = request.form['work_tour']
        else:
            work_tour = "0"
        if request.form.get('work_other'):   
            work_other = request.form['work_other']
        else:
            work_other = "0"
        if request.form.get('work_other_text'):   
            work_other_text = request.form['work_other_text']
        else:
            work_other_text = ""
        
       
    
        if token in valid_tokens:
            new_entry = access_log_DB(
                token = token, 
                action = action, 
                name = name, 
                affiliation = affiliation,
                nr_people = nr_people,
                work_inspection = work_inspection,
                work_maintenance = work_maintenance,
                work_equipment = work_equipment,
                work_sampling = work_sampling,
                work_measurements = work_measurements,
                work_drone = work_drone,
                work_tour = work_tour,
                work_other = work_other,
                work_other_text = work_other_text
                )

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/login_success')
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
        return render_template('login_form.html', swipes=swipes)

@app.route('/logout_form', methods=['POST', 'GET'])
def logout_form():
    error = False
    errorDE = None
    errorEN = None
    valid_tokens = ['t', '0001101747' , '0001964054', '0014488389', '0014405751', '0004033874', '0014580266', '0001951950', '0007000492', '0014502443', '0014552070', '0011248286', '0011248301', '0011250890', '0003912831', '0003858707', '0015466677', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087']

    if request.method == 'POST':
        token = request.form['token']
        action = request.form['action']
        name = request.form['name']
        affiliation = request.form['affiliation'] 
        nr_people = request.form['nr_people'] 
        work_inspection = request.form['work_inspection']
        work_maintenance = request.form['work_maintenance']
        work_equipment = request.form['work_equipment']
        work_sampling = request.form['work_sampling']
        work_measurements = request.form['work_measurements']
        work_drone = request.form['work_drone']
        work_tour = request.form['work_tour']
        work_other = request.form['work_other']
        work_other_text = request.form['work_other_text']
    
        if token in valid_tokens:
            new_entry = access_log_DB(
                token = token, 
                action = action, 
                name = name, 
                affiliation = affiliation,
                nr_people = nr_people,
                work_inspection = work_inspection,
                work_maintenance = work_maintenance,
                work_equipment = work_equipment,
                work_sampling = work_sampling,
                work_measurements = work_measurements,
                work_drone = work_drone,
                work_tour = work_tour,
                work_other = work_other,
                work_other_text = work_other_text
                )

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/logout_success')
            except:
                return 'Could not write to data base.'

        else:
            error = True
            errorDE = 'Dieser Dongle kann nicht gelesen werden. Bitte einen der gültigen Dongles scannen.'
            errorEN = 'This dongle cannot be read, please scan one of provided dongles.'
            return render_template('/invalid.html', error = error, errorDE = errorDE, errorEN = errorEN)

    else:
        # render logout_form page
        return render_template('logout_form.html')

@app.route('/login_success')
def login_success():
    with app.open_resource('static/pincode.txt', 'r') as f:
        pincode = f.read()
    return render_template('login_success.html', pincode = pincode)

@app.route('/logout_success')
def logout_success():
    return render_template('logout_success.html')

@app.route('/admin_index')
def admin_index():
    return render_template('admin_index.html')  

@app.route('/admin_login_form', methods=['POST', 'GET'])
def admin_login_form():
    error = False
    errorDE = None
    errorEN = None

    # get admin token data from CSV file
    admin_tokens = pd.read_csv('static/admin-tokens.csv')  
    admin01_token = admin_tokens.iat[0,0]
    admin01_name = admin_tokens.iat[0,1]
    admin01_affiliation = admin_tokens.iat[0,2]
    admin02_token = admin_tokens.iat[1,0]
    admin02_name = admin_tokens.iat[1,1]
    admin02_affiliation = admin_tokens.iat[1,2]
    admin03_token = admin_tokens.iat[2,0]
    admin03_name = admin_tokens.iat[2,1]
    admin03_affiliation = admin_tokens.iat[2,2]
    admin04_token = admin_tokens.iat[3,0]
    admin04_name = admin_tokens.iat[3,1]
    admin04_affiliation = admin_tokens.iat[3,2]
    admin05_token = admin_tokens.iat[4,0]
    admin05_name = admin_tokens.iat[4,1]
    admin05_affiliation = admin_tokens.iat[4,2]
    admin06_token = admin_tokens.iat[5,0]
    admin06_name = admin_tokens.iat[5,1]
    admin06_affiliation = admin_tokens.iat[5,2]
    admin07_token = admin_tokens.iat[6,0]
    admin07_name = admin_tokens.iat[6,1]
    admin07_affiliation = admin_tokens.iat[6,2]
    admin08_token = admin_tokens.iat[7,0]
    admin08_name = admin_tokens.iat[7,1]
    admin08_affiliation = admin_tokens.iat[7,2]
    admin09_token = admin_tokens.iat[8,0]
    admin09_name = admin_tokens.iat[8,1]
    admin09_affiliation = admin_tokens.iat[8,2]
    admin10_token = admin_tokens.iat[9,0]
    admin10_name = admin_tokens.iat[9,1]
    admin10_affiliation = admin_tokens.iat[9,2]
    admin00_token = admin_tokens.iat[10,0]
    admin00_name = admin_tokens.iat[10,1]
    admin00_affiliation = admin_tokens.iat[10,2]

    admin_tokens = ['a', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087', '0015466677']

    if request.method == 'POST':
        scanned_token = request.form['token']
        action = request.form['action']
        nr_people = request.form['nr_people']
        if request.form.get('work_inspection'):   
            work_inspection = request.form['work_inspection']
        else:
            work_inspection = "0"
        if request.form.get('work_maintenance'):   
            work_maintenance = request.form['work_maintenance']
        else:
            work_maintenance = "0"
        if request.form.get('work_equipment'):   
            work_equipment = request.form['work_equipment']
        else:
            work_equipment = "0"
        if request.form.get('work_sampling'):   
            work_sampling = request.form['work_sampling']
        else:
            work_sampling = "0"
        if request.form.get('work_measurements'):   
            work_measurements = request.form['work_measurements']
        else:
            work_measurements = "0"
        if request.form.get('work_drone'):   
            work_drone = request.form['work_drone']
        else:
            work_drone = "0"
        if request.form.get('work_tour'):   
            work_tour = request.form['work_tour']
        else:
            work_tour = "0"
        if request.form.get('work_other'):   
            work_other = request.form['work_other']
        else:
            work_other = "0"
        if request.form.get('work_other_text'):   
            work_other_text = request.form['work_other_text']
        else:
            work_other_text = ""

        admin_name = 'NA'
        if scanned_token == admin00_token:
            admin_name = admin00_name
        elif scanned_token == admin01_token:
            admin_name = admin01_name
        elif scanned_token == admin02_token:
            admin_name = admin02_name
        elif scanned_token == admin03_token:
            admin_name = admin03_name
        elif scanned_token == admin04_token:
            admin_name = admin04_name
        elif scanned_token == admin05_token:
            admin_name = admin05_name
        elif scanned_token == admin06_token:
            admin_name = admin06_name
        elif scanned_token == admin07_token:
            admin_name = admin07_name
        elif scanned_token == admin08_token:
            admin_name = admin08_name
        elif scanned_token == admin09_token:
            admin_name = admin09_name
        elif scanned_token == admin10_token:
            admin_name = admin10_name         

        admin_affiliation = 'NA'
        if scanned_token == admin00_token:
            admin_affiliation = admin00_affiliation
        elif scanned_token == admin01_token:
            admin_affiliation = admin01_affiliation
        elif scanned_token == admin02_token:
            admin_affiliation = admin02_affiliation
        elif scanned_token == admin03_token:
            admin_affiliation = admin03_affiliation
        elif scanned_token == admin04_token:
            admin_affiliation = admin04_affiliation
        elif scanned_token == admin05_token:
            admin_affiliation = admin05_affiliation
        elif scanned_token == admin06_token:
            admin_affiliation = admin06_affiliation
        elif scanned_token == admin07_token:
            admin_affiliation = admin07_affiliation
        elif scanned_token == admin08_token:
            admin_affiliation = admin08_affiliation
        elif scanned_token == admin09_token:
            admin_affiliation = admin09_affiliation
        elif scanned_token == admin10_token:
            admin_affiliation = admin10_affiliation  
    
        if scanned_token in admin_tokens:
            new_entry = access_log_DB(
                token = scanned_token, 
                action = action, 
                name = admin_name, 
                affiliation = admin_affiliation,
                nr_people = nr_people,
                work_inspection = work_inspection,
                work_maintenance = work_maintenance,
                work_equipment = work_equipment,
                work_sampling = work_sampling,
                work_measurements = work_measurements,
                work_drone = work_drone,
                work_tour = work_tour,
                work_other = work_other,
                work_other_text = work_other_text
                )

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/admin_login_success')
            except:
                return 'Could not write to data base.'

        else:
            error = True
            errorDE = 'Dieser Dongle kann nicht gelesen werden. Bitte einen der gültigen Dongles scannen.'
            errorEN = 'This dongle cannot be read, please scan one of provided dongles.'
            return render_template('/invalid.html', error = error, errorDE = errorDE, errorEN = errorEN)

    else:
        return render_template('admin_login_form.html')
      

@app.route('/admin_logout_form', methods=['POST', 'GET'])
def admin_logout_form():
    error = False
    errorDE = None
    errorEN = None
    admin_tokens = ['a', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087', '0015466677']

    if request.method == 'POST':
        token = request.form['token']
        action = request.form['action']
        name = request.form['name']
        affiliation = request.form['affiliation']
        nr_people = request.form['nr_people']
        work_inspection = request.form['work_inspection']
        work_maintenance = request.form['work_maintenance']
        work_equipment = request.form['work_equipment']
        work_sampling = request.form['work_sampling']
        work_measurements = request.form['work_measurements']
        work_drone = request.form['work_drone']
        work_tour = request.form['work_tour']
        work_other = request.form['work_other']
        work_other_text = request.form['work_other_text']
    
        if token in admin_tokens:
            new_entry = access_log_DB(
                token = token, 
                action = action, 
                name = name, 
                affiliation = affiliation,
                nr_people = nr_people,
                work_inspection = work_inspection,
                work_maintenance = work_maintenance,
                work_equipment = work_equipment,
                work_sampling = work_sampling,
                work_measurements = work_measurements,
                work_drone = work_drone,
                work_tour = work_tour,
                work_other = work_other,
                work_other_text = work_other_text
                )

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/admin_logout_success')
            except:
                return 'Could not write to data base.'

        else:
            error = True
            errorDE = 'Dieser Dongle kann nicht gelesen werden. Bitte einen der gültigen Dongles scannen.'
            errorEN = 'This dongle cannot be read, please scan one of provided dongles.'
            return render_template('/invalid.html', error = error, errorDE = errorDE, errorEN = errorEN)

    else:
        # render logout_form page
        return render_template('admin_logout_form.html')

@app.route('/admin_login_success', methods=['POST', 'GET'])
def admin_login_success():
    with app.open_resource('static/pincode.txt', 'r') as f:
        pincode = f.read()
    return render_template('admin_login_success.html', pincode = pincode)

@app.route('/admin_logout_success', methods=['POST', 'GET'])
def admin_logout_success():
    return render_template('admin_logout_success.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')    

@app.route('/admin_systime', methods=['POST', 'GET'])
def admin_systime():
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return render_template('admin_systime.html', date_time=date_time)      

@app.route('/admin_uptime', methods=['POST', 'GET'])
def admin_uptime():
    uptime =os.popen('uptime -p').read()[:-1] # time since boot
    return render_template('admin_uptime.html', uptime=uptime)    

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
    nr_people = access_log_DB.query.with_entities(access_log_DB.nr_people).order_by(access_log_DB.datetime.desc()).all()
    action = access_log_DB.query.with_entities(access_log_DB.action).order_by(access_log_DB.datetime.desc()).all()
    work_inspection = access_log_DB.query.with_entities(access_log_DB.work_inspection).order_by(access_log_DB.datetime.desc()).all()
    work_maintenance = access_log_DB.query.with_entities(access_log_DB.work_maintenance).order_by(access_log_DB.datetime.desc()).all()
    work_equipment = access_log_DB.query.with_entities(access_log_DB.work_equipment).order_by(access_log_DB.datetime.desc()).all()
    work_sampling = access_log_DB.query.with_entities(access_log_DB.work_sampling).order_by(access_log_DB.datetime.desc()).all()
    work_measurements = access_log_DB.query.with_entities(access_log_DB.work_measurements).order_by(access_log_DB.datetime.desc()).all()
    work_drone = access_log_DB.query.with_entities(access_log_DB.work_drone).order_by(access_log_DB.datetime.desc()).all()
    work_tour = access_log_DB.query.with_entities(access_log_DB.work_tour).order_by(access_log_DB.datetime.desc()).all()
    work_other = access_log_DB.query.with_entities(access_log_DB.work_other).order_by(access_log_DB.datetime.desc()).all()
    work_other_text = access_log_DB.query.with_entities(access_log_DB.work_other_text).order_by(access_log_DB.datetime.desc()).all()

    excel.init_excel(app)
    extension_type = "csv"
    now = time.strftime("%Y%m%d-%H%M%S")
    filename = now + "_fgd_accesslog" + "." + extension_type
    d = {'action': action, 'affiliation': affiliation, 'name': name, 'token': token, 'datetime': datetime, 'id': id, 'nr_people': nr_people, 'work_inspection': work_inspection, 'work_maintenance': work_maintenance, 'work_equipment': work_equipment, 'work_sampling': work_sampling, 'work_measurements': work_measurements, 'work_drone': work_drone, 'work_tour': work_tour, 'work_other': work_other, 'work_other_text': work_other_text}
    src_dir = "/home/pi/Downloads/"
    dst_dir = "/home/pi/Downloads/archived/"
    try:
        os.makedirs(dst_dir);
    except:
        print("Folder already exist.");    
    for csv_file in glob.glob(src_dir + "/*_fgd_accesslog.csv"):
        shutil.copy2(csv_file, dst_dir);
        os.remove(csv_file);
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)

@app.route('/pincode_form', methods=['POST', 'GET'])
def pincode_form():
    if request.method == 'POST':
        pincode_1 = request.form['pincode_1']
        pincode_2 = request.form['pincode_2']
        pincode_3 = request.form['pincode_3']
        pincode_4 = request.form['pincode_4']
        pincode_new = str(pincode_1) + str(pincode_2) + str(pincode_3) + str(pincode_4)
        with open("static/pincode.txt", "w") as fo:
            fo.writelines(pincode_new)
            fo.close()
        return redirect(url_for('pincode_success'))
    else:     
        with app.open_resource('static/pincode.txt', 'r') as f:
            pincode = f.read()
        return render_template('pincode_form.html', pincode = pincode)

@app.route('/pincode_success', methods=['POST', 'GET'])
def pincode_success():
    with app.open_resource('static/pincode.txt', 'r') as f:
        pincode = f.read()
    return render_template('pincode_success.html', pincode = pincode)



@app.route('/admin_tokens', methods=['POST', 'GET'])
def admin_tokens():
    admin_tokens = pd.read_csv('static/admin-tokens.csv')
    
    admin01_token = admin_tokens.iat[0,0]
    admin01_name = admin_tokens.iat[0,1]
    admin01_affiliation = admin_tokens.iat[0,2]
    admin02_token = admin_tokens.iat[1,0]
    admin02_name = admin_tokens.iat[1,1]
    admin02_affiliation = admin_tokens.iat[1,2]
    admin03_token = admin_tokens.iat[2,0]
    admin03_name = admin_tokens.iat[2,1]
    admin03_affiliation = admin_tokens.iat[2,2]
    admin04_token = admin_tokens.iat[3,0]
    admin04_name = admin_tokens.iat[3,1]
    admin04_affiliation = admin_tokens.iat[3,2]
    admin05_token = admin_tokens.iat[4,0]
    admin05_name = admin_tokens.iat[4,1]
    admin05_affiliation = admin_tokens.iat[4,2]
    admin06_token = admin_tokens.iat[5,0]
    admin06_name = admin_tokens.iat[5,1]
    admin06_affiliation = admin_tokens.iat[5,2]
    admin07_token = admin_tokens.iat[6,0]
    admin07_name = admin_tokens.iat[6,1]
    admin07_affiliation = admin_tokens.iat[6,2]
    admin08_token = admin_tokens.iat[7,0]
    admin08_name = admin_tokens.iat[7,1]
    admin08_affiliation = admin_tokens.iat[7,2]
    admin09_token = admin_tokens.iat[8,0]
    admin09_name = admin_tokens.iat[8,1]
    admin09_affiliation = admin_tokens.iat[8,2]
    admin10_token = admin_tokens.iat[9,0]
    admin10_name = admin_tokens.iat[9,1]
    admin10_affiliation = admin_tokens.iat[9,2]
    admin00_token = admin_tokens.iat[10,0]
    admin00_name = admin_tokens.iat[10,1]
    admin00_affiliation = admin_tokens.iat[10,2]

    return render_template('admin_tokens.html', 
    admin_tokens = admin_tokens, 
    admin01_token = admin01_token,
    admin01_name = admin01_name,
    admin01_affiliation = admin01_affiliation, 
    admin02_token = admin02_token,
    admin02_name = admin02_name,
    admin02_affiliation = admin02_affiliation, 
    admin03_token = admin03_token,
    admin03_name = admin03_name,
    admin03_affiliation = admin03_affiliation, 
    admin04_token = admin04_token,
    admin04_name = admin04_name,
    admin04_affiliation = admin04_affiliation, 
    admin05_token = admin05_token,
    admin05_name = admin05_name,
    admin05_affiliation = admin05_affiliation, 
    admin06_token = admin06_token,
    admin06_name = admin06_name,
    admin06_affiliation = admin06_affiliation, 
    admin07_token = admin07_token,
    admin07_name = admin07_name,
    admin07_affiliation = admin07_affiliation, 
    admin08_token = admin08_token,
    admin08_name = admin08_name,
    admin08_affiliation = admin08_affiliation, 
    admin09_token = admin09_token,
    admin09_name = admin09_name,
    admin09_affiliation = admin09_affiliation, 
    admin10_token = admin10_token,
    admin10_name = admin10_name,
    admin10_affiliation = admin10_affiliation, 
    admin00_token = admin00_token,
    admin00_name = admin00_name,
    admin00_affiliation = admin00_affiliation)



@app.route('/admin_token_assign_01', methods=['POST', 'GET'])
def admin_token_assign_01():
    if request.method == 'POST':

        # get new values from form
        admin01_token = request.form['admin01_token_assigned']
        admin01_name = request.form['admin01_name_assigned']
        admin01_affiliation = request.form['admin01_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]        

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2] 
               
        return render_template('admin_token_assign_01.html', 
        admin01_token = admin01_token,
        admin01_name = admin01_name,
        admin01_affiliation = admin01_affiliation)


@app.route('/admin_token_assign_02', methods=['POST', 'GET'])
def admin_token_assign_02():
    if request.method == 'POST':

        # get new values from form
        admin02_token = request.form['admin02_token_assigned']
        admin02_name = request.form['admin02_name_assigned']
        admin02_affiliation = request.form['admin02_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2] 
               
        return render_template('admin_token_assign_02.html', 
        admin02_token = admin02_token,
        admin02_name = admin02_name,
        admin02_affiliation = admin02_affiliation)

@app.route('/admin_token_assign_03', methods=['POST', 'GET'])
def admin_token_assign_03():
    if request.method == 'POST':

        # get new values from form
        admin03_token = request.form['admin03_token_assigned']
        admin03_name = request.form['admin03_name_assigned']
        admin03_affiliation = request.form['admin03_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2] 
               
        return render_template('admin_token_assign_03.html', 
        admin03_token = admin03_token,
        admin03_name = admin03_name,
        admin03_affiliation = admin03_affiliation)

@app.route('/admin_token_assign_04', methods=['POST', 'GET'])
def admin_token_assign_04():
    if request.method == 'POST':

        # get new values from form
        admin04_token = request.form['admin04_token_assigned']
        admin04_name = request.form['admin04_name_assigned']
        admin04_affiliation = request.form['admin04_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2] 
               
        return render_template('admin_token_assign_04.html', 
        admin04_token = admin04_token,
        admin04_name = admin04_name,
        admin04_affiliation = admin04_affiliation)

@app.route('/admin_token_assign_05', methods=['POST', 'GET'])
def admin_token_assign_05():
    if request.method == 'POST':

        # get new values from form
        admin05_token = request.form['admin05_token_assigned']
        admin05_name = request.form['admin05_name_assigned']
        admin05_affiliation = request.form['admin05_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2] 
               
        return render_template('admin_token_assign_05.html', 
        admin05_token = admin05_token,
        admin05_name = admin05_name,
        admin05_affiliation = admin05_affiliation)

@app.route('/admin_token_assign_06', methods=['POST', 'GET'])
def admin_token_assign_06():
    if request.method == 'POST':

        # get new values from form
        admin06_token = request.form['admin06_token_assigned']
        admin06_name = request.form['admin06_name_assigned']
        admin06_affiliation = request.form['admin06_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2] 
               
        return render_template('admin_token_assign_06.html', 
        admin06_token = admin06_token,
        admin06_name = admin06_name,
        admin06_affiliation = admin06_affiliation)

@app.route('/admin_token_assign_07', methods=['POST', 'GET'])
def admin_token_assign_07():
    if request.method == 'POST':

        # get new values from form
        admin07_token = request.form['admin07_token_assigned']
        admin07_name = request.form['admin07_name_assigned']
        admin07_affiliation = request.form['admin07_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2] 
               
        return render_template('admin_token_assign_07.html', 
        admin07_token = admin07_token,
        admin07_name = admin07_name,
        admin07_affiliation = admin07_affiliation)

@app.route('/admin_token_assign_08', methods=['POST', 'GET'])
def admin_token_assign_08():
    if request.method == 'POST':

        # get new values from form
        admin08_token = request.form['admin08_token_assigned']
        admin08_name = request.form['admin08_name_assigned']
        admin08_affiliation = request.form['admin08_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2] 
               
        return render_template('admin_token_assign_08.html', 
        admin08_token = admin08_token,
        admin08_name = admin08_name,
        admin08_affiliation = admin08_affiliation)

@app.route('/admin_token_assign_09', methods=['POST', 'GET'])
def admin_token_assign_09():
    if request.method == 'POST':

        # get new values from form
        admin09_token = request.form['admin09_token_assigned']
        admin09_name = request.form['admin09_name_assigned']
        admin09_affiliation = request.form['admin09_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2] 
               
        return render_template('admin_token_assign_09.html', 
        admin09_token = admin09_token,
        admin09_name = admin09_name,
        admin09_affiliation = admin09_affiliation)

@app.route('/admin_token_assign_10', methods=['POST', 'GET'])
def admin_token_assign_10():
    if request.method == 'POST':

        # get new values from form
        admin10_token = request.form['admin10_token_assigned']
        admin10_name = request.form['admin10_name_assigned']
        admin10_affiliation = request.form['admin10_affiliation_assigned']

        # create dictionary from form responses, then convert to data frame
        response_dict = request.form.to_dict()
        response_df = pd.DataFrame([response_dict.values()], columns=response_dict.keys())

        # get unchanged values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin02_token = admin_tokens.iat[1,0]
        admin02_name = admin_tokens.iat[1,1]
        admin02_affiliation = admin_tokens.iat[1,2]
        admin03_token = admin_tokens.iat[2,0]
        admin03_name = admin_tokens.iat[2,1]
        admin03_affiliation = admin_tokens.iat[2,2]
        admin04_token = admin_tokens.iat[3,0]
        admin04_name = admin_tokens.iat[3,1]
        admin04_affiliation = admin_tokens.iat[3,2]
        admin05_token = admin_tokens.iat[4,0]
        admin05_name = admin_tokens.iat[4,1]
        admin05_affiliation = admin_tokens.iat[4,2]
        admin06_token = admin_tokens.iat[5,0]
        admin06_name = admin_tokens.iat[5,1]
        admin06_affiliation = admin_tokens.iat[5,2]
        admin07_token = admin_tokens.iat[6,0]
        admin07_name = admin_tokens.iat[6,1]
        admin07_affiliation = admin_tokens.iat[6,2]
        admin08_token = admin_tokens.iat[7,0]
        admin08_name = admin_tokens.iat[7,1]
        admin08_affiliation = admin_tokens.iat[7,2]
        admin09_token = admin_tokens.iat[8,0]
        admin09_name = admin_tokens.iat[8,1]
        admin09_affiliation = admin_tokens.iat[8,2]
        admin01_token = admin_tokens.iat[0,0]
        admin01_name = admin_tokens.iat[0,1]
        admin01_affiliation = admin_tokens.iat[0,2]
        admin00_token = admin_tokens.iat[10,0]
        admin00_name = admin_tokens.iat[10,1]
        admin00_affiliation = admin_tokens.iat[10,2]

        # merge current and new token assignments
        dongles = [admin01_token, admin02_token, admin03_token, admin04_token, admin05_token, 
        admin06_token, admin07_token, admin08_token, admin09_token, admin10_token, admin00_token] 
        names = [admin01_name, admin02_name, admin03_name, admin04_name, admin05_name, 
        admin06_name, admin07_name, admin08_name, admin09_name, admin10_name, admin00_name] 
        affiliations = [admin01_affiliation, admin02_affiliation, admin03_affiliation, admin04_affiliation, admin05_affiliation, 
        admin06_affiliation, admin07_affiliation, admin08_affiliation, admin09_affiliation, admin10_affiliation, admin00_affiliation] 

        # create dataframe with new tokens
        new_tokens_list = [
            [admin01_token, admin01_name, admin01_affiliation],
            [admin02_token, admin02_name, admin02_affiliation],
            [admin03_token, admin03_name, admin03_affiliation],
            [admin04_token, admin04_name, admin04_affiliation],
            [admin05_token, admin05_name, admin05_affiliation],
            [admin06_token, admin06_name, admin06_affiliation],
            [admin07_token, admin07_name, admin07_affiliation],
            [admin08_token, admin08_name, admin08_affiliation],
            [admin09_token, admin09_name, admin09_affiliation],
            [admin10_token, admin10_name, admin10_affiliation],
            [admin00_token, admin00_name, admin00_affiliation]
            ]
        new_tokens_df = pd.DataFrame(new_tokens_list, columns = ['dongle', 'name', 'affiliation'])

        # export to CSV
        new_tokens_df.to_csv('static/admin-tokens.csv', encoding='utf-8', index=False)

        return redirect(url_for('admin_tokens'))

    else:  

        # get current values from CSV file
        admin_tokens = pd.read_csv('static/admin-tokens.csv')  
        admin10_token = admin_tokens.iat[9,0]
        admin10_name = admin_tokens.iat[9,1]
        admin10_affiliation = admin_tokens.iat[9,2] 
               
        return render_template('admin_token_assign_10.html', 
        admin10_token = admin10_token,
        admin10_name = admin10_name,
        admin10_affiliation = admin10_affiliation)


@app.route('/admin_data2usb', methods=['POST', 'GET'])
def admin_data2usb():  
    return render_template('admin_data2usb.html')

@app.route('/data2usb')
def data2usb(): 
    os.system("sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi")
    os.system("cp -r /home/pi/Downloads/* /media/usb/")
    os.system("sudo umount /media/usb/")
    return redirect(url_for('admin'))
    

@app.route('/reboot')
def reboot():
    os.system("sudo shutdown -r now")
    
@app.route('/shutdown')
def shutdown():
    os.system("sudo shutdown -h now")

@app.route('/email_form', methods=['POST', 'GET'])
def email_form():  
    if request.method == 'POST':
        return redirect(url_for('email_success'))
    else:     
        return render_template('email_form.html')
        
@app.route('/email_success', methods=['POST', 'GET'])
def email_success():
    # TODO check for WiFi
    email_address = request.form['email_address']
    src_dir = "/home/pi/Downloads/"
    attachments_all = glob.glob(src_dir + "/*_fgd_accesslog.csv")
    attachments_first = attachments_all[0] 
    msg = Message(subject = 'UFZ FGD: Access Log', sender = 'fgd-accesslog@outlook.com', recipients = [email_address])
    msg.body = "Please find attached the most recent copy of the UFZ Research Green Roof Access Log database.\n\nNOTE: This email account is unsupervised. Do not reply."
    # TODO send the latest copy
    with open(attachments_first, "rb") as fp:
        msg.attach(os.path.basename(attachments_first), "text/csv", fp.read())
    mail.send(msg)
    return render_template('email_success.html', email_address=email_address)  

# Debugger
#=====================================================  

if __name__ == "__main__":
     app.run(debug=True)


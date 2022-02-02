from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

import flask_excel as excel
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
    admin_tokens = ['a', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087', '0015466677']

    if request.method == 'POST':
        token = request.form['token']
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

        name = 'NA'
        if token == 'a':
            name = 'Test-Admin'
        elif token == '0015465087':
            name = 'Jan Knappe'
        elif token == '0004498655':
            name = 'Lucie Moeller'
        elif token == '0015465203':
            name = 'Katy Bernhard'
        elif token == '0004656070':
            name = 'Max Ueberham'
        elif token == '0003949645':
            name = 'Ralf Trabitzsch'
        elif token == '0004484801':
            name = 'Niels Wollschläger'
        elif token == '0015466677':
            name = 'Christian Hecht'
        elif token == '0004724076':
            name = 'Peter Otto'
        elif token == '0004499470':
            name = 'Admin 9'
        elif token == '0015465255':
            name = 'Admin 10'          

        affiliation = 'NA'
        if token == 'a':
            affiliation = 'Test-Admin'
        elif token == '0015465087':
            affiliation = 'UFZ UBZ'
        elif token == '0004498655':
            affiliation = 'UFZ UBZ'
        elif token == '0015465203':
            affiliation = 'UFZ UBZ'
        elif token == '0004656070':
            affiliation = 'UFZ UBZ'
        elif token == '0003949645':
            affiliation = 'UFZ ENVINF'
        elif token == '0004484801':
            affiliation = 'UFZ SUSOZ'
        elif token == '0015466677':
            affiliation = 'UFZ NSF'
        elif token == '0004724076':
            affiliation = 'Uni Leipzig'
        elif token == '0004499470':
            affiliation = 'Admin 9'
        elif token == '0015465255':
            affiliation = 'Admin 10'    
    
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


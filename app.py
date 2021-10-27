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
app.config['MAIL_PASSWORD'] = os.environ['email_pw']
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
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id %r>' % self.id

# Set up rendered pages and functions
#=====================================================  

@app.route('/', methods=['POST', 'GET'])
def index():
    admin_input = ['admin']
    
    if request.method == 'POST':
        user_input = request.form['token']
        if user_input in admin_input:
            return render_template('admin_check.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/login_form', methods=['POST', 'GET'])
def login_form():
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
    
        if token in valid_tokens:
            new_entry = access_log_DB(token = token, action = action, name = name, affiliation = affiliation)

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
    return render_template('login_success.html')

@app.route('/logout_success')
def logout_success():
    return render_template('logout_success.html')

@app.route('/admin_check', methods=['POST', 'GET'])
def admin_check():
    admin_tokens = ['admin', '0004484801', '0003949645', '0004656070', '0004499470', '0015465255', '0004498655', '0004724076', '0015465203', '0015465087']

    if request.method == 'POST':
        token = request.form['token']
    
        if token in admin_tokens:
            return render_template('admin.html') 
        else:
            return render_template('admin_check.html')  
            
    else:
        return render_template('admin_check.html')  

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')    

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
    now = time.strftime("%Y%m%d-%H%M%S")
    filename = now + "_fgd_accesslog" + "." + extension_type
    d = {'action': action, 'affiliation': affiliation, 'name': name, 'token': token, 'datetime': datetime, 'id': id}
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


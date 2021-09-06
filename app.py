from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

@app.route('/ascend', methods=['POST', 'GET'])
def ascend():
    error = None
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
                return redirect('/success')
            except:
                return 'Could not write to data base.'

        else:
            error = 'The token you scanned is not registered, please use one of the valid access tokens.'
            ## swipes = access_log.query.order_by(access_log.datetime.desc()).all()
            return render_template('/invalid.html', error = error) # redirect to 'invalid.html', error=error

    else:
        # read swipes data from the database
        swipes = access_log_DB.query.order_by(access_log_DB.datetime.desc()).all()
        # render the index pages with swipes data available
        return render_template('ascend.html', swipes=swipes)

@app.route('/admin')
def admin():
    swipes = access_log_DB.query.order_by(access_log_DB.datetime.desc()).all()
    return render_template('admin.html', swipes=swipes)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
     app.run(debug=True)
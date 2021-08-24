from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///access-log.db'
app.secret_key = 'fgd2L"))+=23F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class token_scan_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(20), nullable=False)
    datetime_scanned = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    valid_tokens = ['t', '0001101747' , '0001964054', '0014488389', '0014405751', '0004033874', '0014580266', '0001951950', '0007000492', '0014502443', '0014552070']

    if request.method == 'POST':
        token_id = request.form['token_id']
    
        if token_id == 'admin':
            return redirect('/admin')
        else:
            if token_id in valid_tokens:
                new_token = FormDB(token_id=token_id)

                try:
                    db.session.add(new_token)
                    db.session.commit()
                    return redirect('/form')
                except:
                    return 'Could not write to data base.'
            else:
                error = 'The token you scanned is not registered, please use one of the valid access tokens.'
                swipes = FormDB.query.order_by(FormDB.datetime_scanned.desc()).all()
                return render_template('invalid.html', error=error)

    else:
        # read swipes data from the database
        swipes = FormDB.query.order_by(FormDB.datetime_scanned.desc()).all()
        # render the index pages with swipes data available
        return render_template('index.html', swipes=swipes)

if __name__ == "__main__":
     app.run(debug=True)
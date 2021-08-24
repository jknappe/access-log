from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///access-log.db'
app.secret_key = 'fgd2L"))+=23F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class token_scan_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(20), nullable=False)
    token = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    # render index page
    return render_template('index.html')

if __name__ == "__main__":
     app.run(debug=True)
from datetime import datetime
import os
from flask import Flask, render_template, request, url_for, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studyhours = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    classname = db.Column(db.String(25), unique=False, nullable=True)
    comment = db.Column(db.String(50), unique=False, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    # bio = db.Column(db.Text)

    def __repr__(self):
        return f'<StudyLog {self.id}>'

# ! ---------------------- ROUTES ---------------------- !

@app.route('/')
@app.route('/index')
def index():
    studylog = StudyLog.query.all()
    return render_template('index.html', studylog=studylog, title='Home')

@app.route('/submit_hours', methods=('GET', 'POST'))
def create():
    date_format = "%Y-%m-%d"

    if request.method == 'POST':
        studyhours = int(request.form['studyhours'])
        date_string = request.form['date']
        date = datetime.strptime(date_string, date_format)
        classname = request.form['classname']
        comment = request.form['comment']
        studylog = StudyLog(studyhours=studyhours,
                        date=date,
                        classname=classname,
                        comment=comment)
        db.session.add(studylog)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('submit_hours.html')
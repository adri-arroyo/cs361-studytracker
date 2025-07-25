from datetime import datetime
import os
from flask import Flask, render_template, request, url_for, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='./static')
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studyhours = db.Column(db.Numeric(12, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    classname = db.Column(db.String(25), unique=False, nullable=True)
    comment = db.Column(db.String(50), unique=False, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    # bio = db.Column(db.Text)

    def __repr__(self):
        return f'<StudyLog {self.id}>'

# ! ---------------------- ROUTES ---------------------- !
date_format = "%Y-%m-%d"

@app.route('/')
@app.route('/index')
def index():
    studylog = StudyLog.query.all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')

@app.route('/index/sort_by_date_desc', methods=('GET', 'POST'))
def sort_by_date_desc():
    studylog = StudyLog.query.order_by(StudyLog.date.desc()).all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')

@app.route('/index/sort_by_date_asc', methods=('GET', 'POST'))
def sort_by_date_asc():
    studylog = StudyLog.query.order_by(StudyLog.date.asc()).all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')

@app.route('/index/sort_by_hrs_desc', methods=('GET', 'POST'))
def sort_by_hrs_desc():
    studylog = StudyLog.query.order_by(StudyLog.studyhours.desc()).all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')

@app.route('/index/sort_by_hrs_asc', methods=('GET', 'POST'))
def sort_by_hrs_asc():
    studylog = StudyLog.query.order_by(StudyLog.studyhours.asc()).all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')

@app.route('/index/sort_by/<class_name>', methods=('GET', 'POST'))
def sort_by_class_name(class_name):
    # studylog = StudyLog.query.get_or_404(class_name)


    studylog = StudyLog.query.filter_by(classname=class_name).all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')
    
    # studylog = StudyLog.query.all()
    # return render_template('index.html', studylog=studylog)

@app.route('/submit_hours', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        studyhours = float(request.form['studyhours'])
        date_string = request.form['date']
        date = datetime.strptime(date_string, date_format).date()
        classname = request.form['classname']
        comment = request.form['comment']
        studylog = StudyLog(studyhours=studyhours,
                        date=date,
                        classname=classname,
                        comment=comment)
        db.session.add(studylog)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('submit_hours.html', title='Add Study Hours')

@app.route('/edit_hours/<int:log_id>', methods=('GET', 'POST'))
def edit(log_id):
    studylog = StudyLog.query.get_or_404(log_id)

    if request.method == 'POST':
        studyhours = float(request.form['studyhours'])
        date_string = request.form['date']
        date = datetime.strptime(date_string, date_format).date()
        classname = request.form['classname']
        comment = request.form['comment']

        studylog.studyhours = studyhours
        studylog.date = date
        studylog.classname = classname
        studylog.comment = comment

        db.session.add(studylog)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_hours.html', title='Edit Study Hours', studylog=studylog)

@app.post('/delete_hours/<int:log_id>')
def delete(log_id):
    studylog = StudyLog.query.get_or_404(log_id)
    db.session.delete(studylog)
    db.session.commit()
    return redirect(url_for('index'))
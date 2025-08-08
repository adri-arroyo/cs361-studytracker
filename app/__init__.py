from datetime import datetime
import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
import requests
import matplotlib.pyplot as plt

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
    studylog = StudyLog.query.filter_by(classname=class_name).all()
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]
    return render_template('index.html', studylog=studylog, classnames=classnames_list, title='Home')


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



# !------ MICROSERVICE ROUTES --------!

# Microservice A
@app.route('/countdown', methods=('GET', 'POST'))
def calculate_countdown():
    if request.method == 'POST':
        print("Sending data to Microservice A...")

        target_date = request.form['targetDate']
        display_format = request.form['displayFormat']

        data = {'target_date': target_date, 'display_format': display_format}
        response = requests.post('http://127.0.0.1:6000/process', json=data)

        response_data = response.text

        print(f"Received from Microservice A: '{response_data}'")

        return render_template('countdown.html', response_data=response_data)
    return render_template('countdown.html')

# Microservice B
@app.route('/total_hrs', methods=('GET', 'POST'))
def calculate_total_hrs():
    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]

    if request.method == 'POST':
        print("Sending Total Study Hours to Microservice B...")
        log_classname = request.form.get('classname_val')

        if len(log_classname) == 0:
            log_classname = "ALL CLASSES"
            study_hours = StudyLog.query.with_entities(StudyLog.studyhours).all()
            study_hours_list = [studyhours[0] for studyhours in study_hours]
        
        else:
            study_hours = StudyLog.query.filter_by(classname=log_classname).with_entities(StudyLog.studyhours).all()
            study_hours_list = [studyhours[0] for studyhours in study_hours]

        for i, study_hours in enumerate(study_hours_list):
            study_hours_list[i] = str(study_hours)

        data = {'total_hrs': study_hours_list}
        response = requests.post('http://127.0.0.1:7000/calculate_hrs', json=data)

        response_data = response.json()
        total_hrs = response_data["total_hr_sum"]
        print(f"Received total hours from Microservice B: {total_hrs}")

        return render_template('total_hrs.html', totalhrs=total_hrs, classnames=classnames_list, selectedclass=log_classname)
    
    else:
        log_classname = "ALL CLASSES"
        study_hours = StudyLog.query.with_entities(StudyLog.studyhours).all()
        study_hours_list = [studyhours[0] for studyhours in study_hours]
        
        for i, study_hours in enumerate(study_hours_list):
            study_hours_list[i] = str(study_hours)

        data = {'total_hrs': study_hours_list}
        response = requests.post('http://127.0.0.1:7000/calculate_hrs', json=data)

        response_data = response.json()
        total_hrs = response_data["total_hr_sum"]
        print(f"Received total hours from Microservice B: {total_hrs}")

    return render_template('total_hrs.html', classnames=classnames_list, totalhrs=total_hrs, selectedclass=log_classname)

# Microservice C
@app.route('/study_graph', methods=('GET', 'POST'))
def generate_graph():
    graph_info_dict = {}

    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]

    if request.method == 'POST':
        selected_classes = []
        for key, value in request.form.items():
            selected_classes.append(key)
        print(selected_classes)

        for selected_class in selected_classes:

            study_hours = StudyLog.query.filter_by(classname=selected_class).with_entities(StudyLog.studyhours).all()
            study_hours_list = [studyhours[0] for studyhours in study_hours]

            for i, study_hours in enumerate(study_hours_list):
                study_hours_list[i] = str(study_hours)

            data = {'total_hrs': study_hours_list}
            response = requests.post('http://127.0.0.1:7000/calculate_hrs', json=data)

            response_data = response.json()
            total_hrs = response_data["total_hr_sum"]

            graph_info_dict[selected_class] = str(total_hrs)

    else:
        for selected_class in classnames_list:

            study_hours = StudyLog.query.filter_by(classname=selected_class).with_entities(StudyLog.studyhours).all()
            study_hours_list = [studyhours[0] for studyhours in study_hours]

            for i, study_hours in enumerate(study_hours_list):
                study_hours_list[i] = str(study_hours)

            data = {'total_hrs': study_hours_list}
            response = requests.post('http://127.0.0.1:7000/calculate_hrs', json=data)

            response_data = response.json()
            total_hrs = response_data["total_hr_sum"]

            graph_info_dict[selected_class] = str(total_hrs)

    print("Sending Study Graph Request to Microservice C...")
    response = requests.post('http://127.0.0.1:8000/view_graph', json=graph_info_dict)

    if response.status_code == 200:
        with open(r"app\static\images\received_graph.png", "wb") as f:
            f.write(response.content)
        print("Received Study Graph from Microservice C and saved as received_graph.png")
    else:
        print(f"Error: {response.status_code}")
    return render_template('study_graph.html', classnames=classnames_list)

# Microservice C
@app.route('/study_goals', methods=('GET', 'POST'))
def goal_progress():
    goal_info_dict = {}

    classnames = StudyLog.query.with_entities(StudyLog.classname).distinct().all()
    classnames_list = [classname[0] for classname in classnames]

    if request.method == 'POST':
        for key, value in request.form.items():
            goal_info_dict[key] = value

        selected_class = goal_info_dict['class_name']
        study_hours = StudyLog.query.filter_by(classname=selected_class).with_entities(StudyLog.studyhours).all()
        study_hours_list = [studyhours[0] for studyhours in study_hours]

        for i, study_hours in enumerate(study_hours_list):
            study_hours_list[i] = str(study_hours)

        data = {'total_hrs': study_hours_list}
        response = requests.post('http://127.0.0.1:7000/calculate_hrs', json=data)

        response_data = response.json()
        total_hrs = response_data["total_hr_sum"]

        goal_info_dict["study_hrs"] = str(total_hrs)

        print("Sending Study Goal Calculator Request to Microservice D...")
        response = requests.post('http://127.0.0.1:9000/calculate_progress', json=goal_info_dict)

        response_data = response.json()
        goal_progress = response_data["goal_progress"]
        print(f"Received study goal progress from Microservice D: {goal_progress}% Completed")

        return render_template('study_goals.html', classnames=classnames_list, selectedclass=selected_class, goalprogress=goal_progress, classname=goal_info_dict['class_name'])
    
    return render_template('study_goals.html', classnames=classnames_list, goalprogress=-1)
from app import app
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to Microservice C. :)"

@app.route('/calculate_progress', methods=['POST'])
def calculate_progress():
    if request.method == 'POST':
        print("Microservice D successfully received the POST request from Main Program.")
        request_data = request.json

        class_name = request_data["class_name"]
        goal_hours = float(request_data["goal_hours"])
        study_hrs = float(request_data["study_hrs"])

        print(f"    Received Study Goal Parameters: {request_data}")

        goal_progress = int((study_hrs / goal_hours) * 100)

        if goal_progress >= 100:
            goal_progress = 100
        
        data = {"goal_progress" : goal_progress}

        print(f"    Successfully Calculated Goal Progress: {goal_progress}% Completed")
        print("Sending Goal Progress to Main Program...")
        return data
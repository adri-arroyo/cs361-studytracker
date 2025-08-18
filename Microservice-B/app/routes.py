from app import app
from flask import request


@app.route('/')
@app.route('/index')
def index():
    return "Welcome to Microservice B. :)"

@app.route('/calculate_hrs', methods=['GET', 'POST'])
def calculate_hrs():
    if request.method == 'GET':
        print("Microservice B successfully received the GET request from Main Program.")
        # Handle GET request (e.g., return data)
        return "Microservice B successfully received the GET request."
    elif request.method == 'POST':
        print("Microservice B successfully received the POST request from Main Program.")
        request_data = request.json
        total_hrs = request_data["total_hrs"]
        print(f"    Received list of total hours: {total_hrs}")

        total_hr_sum = 0

        for hr in total_hrs:
            total_hr_sum += float(hr)

        data = {"total_hr_sum" : str(total_hr_sum)}
        print(f"    Successfully Calculated Total Hours: {total_hr_sum}")
        print("Sending total hours to Main Program...")
        return data
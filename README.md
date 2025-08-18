
# CS361-StudyTracker

<img alt="Preview of StudyTracker Web Application" src="https://github.com/adri-arroyo/cs361-studytracker/blob/main/StudyTracker-preview.gif" />

The objective of this project was to develop a web application that users can use to log and track their study hours for classes they’re currently taking, measure their progress by setting up study goals, and view visualization summaries of their logged data. The project consists of one Main Application and three additional Microservices that provide additional functionality.

# Features

+ **Customizability:** StudyTracker allows the user to categorize their entries with their corresponding class names, which allows them to  organize and classify their data as they see fit, as these categories can be later used when filtering out the data per class.
+ **Study Hours Calculator:** Users can view the total amount of study hours they have spnt on each class.
+ **Graph Visualizations:** Users can view a graph visualization of their total study hours, or filter out the data to receive a customized graph containing only the classes they have selected.
+ **Set Up and Measure Study Goal Progress:** Users can set up a Study Goal and see how close they are to completing the total amount of hours set up as part of the goal.

## Getting Started

The communication pipeline between the Main Program and the Microservices will be performed using REST API. It is recommended that you run the StudyTracker and the three Microservices on separate terminal instances. Feel free to edit the default values of each application's **.flaskenv** file. 

It is **HIGHLY RECOMMENDED** that you run StudyTracker within a virtual environment. Run the following commands on the directory where the StudyTracker and Microservice folders are located, to create the virtual environment.
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Once inside the virtual environment, make sure to install the following packages before running the app.
```
pip install flask 
pip install python-dotenv
pip install flask-sqlalchemy
pip install requests
pip install matplotlib
```

Once all packages have been installed, run the Main Program and each Microservice using the following command.
```
flask run
```

## Study Tracker Preview
<img alt="Preview of StudyTracker Web Application, Microservice D Functionality" src="https://github.com/adri-arroyo/cs361-studytracker/blob/main/MicroserviceD-preview.gif" />
<img alt="Preview of StudyTracker Web Application, Microservice C Functionality" src="https://github.com/adri-arroyo/cs361-studytracker/blob/main/MicroserviceC-preview.gif" />
<img alt="Preview of StudyTracker Web Application, Microservice B Functionality" src="https://github.com/adri-arroyo/cs361-studytracker/blob/main/MicroserviceB-preview.gif" />

## Acknowledgements

This project was developed as part of the course CS361 - Software Engineering I, at Oregon State University as part of the Summer 2025 term. 
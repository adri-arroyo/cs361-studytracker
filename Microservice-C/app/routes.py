from app import app
from flask import request, send_file
import matplotlib.pyplot as plt
import matplotlib


@app.route('/')
@app.route('/index')
def index():
    return "Welcome to Microservice C. :)"

@app.route('/view_graph', methods=['POST'])
def send_graph():
    if request.method == 'POST':
        print("Microservice C successfully received the POST request from Main Program.")
        request_data = request.json

        print(f"    Received List of Class Hours: {request_data}")

        matplotlib.use('agg')

        labels = []
        sizes = []

        for key, value in request_data.items():
            labels.append(key)
            sizes.append(float(value))

        print(f"    Creating Study Graph for the following classes: {labels}")


        divisor = sum(sizes)
        
        new_sizes = []

        for size in sizes:
            new_sizes.append(int((size/divisor) * 100))

        colors = ["orange", "orangered", "brown", "salmon"]

        fig, ax = plt.subplots()
        ax.pie(new_sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.savefig(r'app\class_pie_chart.png', bbox_inches='tight', transparent=True)

        image_path = 'class_pie_chart.png'

        print(f"    Successfully Created Study Graph Pie Chart.")
        print("Sending Study Graph Pie Chart to Main Program...")
        return send_file(image_path, mimetype='image/png')
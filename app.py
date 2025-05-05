import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__, template_folder="templates")

# Load models correctly using pickle
model = pickle.load(open('model.pkl', 'rb'))
model1 = pickle.load(open('model1.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')  # Changed from 'h.html'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    cgpa = float(request.args.get('cgpa', 0))  # Default to 0 if not provided
    projects = int(request.args.get('projects', 0))  # Convert to integer
    workshops = int(request.args.get('workshops', 0))
    mini_projects = int(request.args.get('mini_projects', 0))
    skills = request.args.get('skills', '')
    communication_skills = float(request.args.get('communication_skills', 0))  # Default to 0
    internship = int(request.args.get('internship', 0))
    hackathon = int(request.args.get('hackathon', 0))
    tw_percentage = float(request.args.get('tw_percentage', 0))
    te_percentage = float(request.args.get('te_percentage', 0))
    backlogs = int(request.args.get('backlogs', 0))
    name = request.args.get('name', 'Student')

    s = len(skills.split(',')) if skills else 0  # Handle skills count

    arr = np.array([cgpa, projects, workshops, mini_projects, s, communication_skills, internship, hackathon, tw_percentage, te_percentage, backlogs])
    brr = np.asarray(arr, dtype=float)

    try:
        output = model.predict([brr])[0]
    except Exception as e:
        return f"Error in prediction: {str(e)}"

    p = '1' if output == 'Placed' else '0'

    arr1 = np.array([cgpa, projects, workshops, mini_projects, s, communication_skills, internship, hackathon, tw_percentage, te_percentage, backlogs, p])
    brr1 = np.asarray(arr1, dtype=float)

    try:
        salary = model1.predict([brr1])[0]
    except Exception as e:
        return f"Error in salary prediction: {str(e)}"

    k = f"{int(salary):,}"

    if output == 'Placed':
        out = f'Congratulations {name} !! You have high chances of getting placed!!!'
        out2 = f'Your Expected Salary will be INR {k} per annum'
    else:
        out = f'Sorry {name} !! You have low chances of getting placed. All the best!!!!'
        out2 = 'Improve your skills...'

    return render_template('output.html', output=out, output2=out2)

if __name__ == "__main__":
    app.run(debug=True)

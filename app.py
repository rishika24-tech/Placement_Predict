import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__, template_folder="templates")

# Load models correctly using pickle
model = pickle.load(open('model.pkl', 'rb'))
model1 = pickle.load(open('model1.pkl', 'rb'))

@app.route('/')
def h():
    return render_template('h.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    cgpa = request.args.get('cgpa') or '0'
    projects = request.args.get('projects') or '0'
    workshops = request.args.get('workshops') or '0'
    mini_projects = request.args.get('mini_projects') or '0'
    skills = request.args.get('skills') or ''
    communication_skills = request.args.get('communication_skills') or '0'
    internship = request.args.get('internship') or '0'
    hackathon = request.args.get('hackathon') or '0'
    tw_percentage = request.args.get('tw_percentage') or '0'
    te_percentage = request.args.get('te_percentage') or '0'
    backlogs = request.args.get('backlogs') or '0'
    name = request.args.get('name') or 'Student'

    s = skills.count(',') + 1 if skills else 0

    arr = np.array([cgpa, projects, workshops, mini_projects, s, communication_skills, internship, hackathon, tw_percentage, te_percentage, backlogs])
    brr = np.asarray(arr, dtype=float)
    output = model.predict([brr])[0]

    p = '1' if output == 'Placed' else '0'

    arr1 = np.array([cgpa, projects, workshops, mini_projects, s, communication_skills, internship, hackathon, tw_percentage, te_percentage, backlogs, p])
    brr1 = np.asarray(arr1, dtype=float)
    salary = model1.predict([brr1])[0]
    k = f"{int(salary):,}"

    if output == 'Placed':
        out = f'Congratulations {name} !! You have high chances of getting placed!!!'
        out2 = f'Your Expected Salary will be INR {k} per annum'
    else:
        out = f'Sorry {name} !! You have low chances of getting placed. All the best!!!!'
        out2 = 'Improve your skills...'

    return render_template('out.html', output=out, output2=out2)

if __name__ == "__main__":
    app.run(debug=True)

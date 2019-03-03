from flask import Flask
from flask import request
from flask import make_response
import random

app = Flask(__name__)
p1 = ''
p2 = ''
redux_table = {('C','C'): ('5','5'), ('C', 'B'): ('2','3'), ('B', 'C'): ('3','2'), ('B','B'): ('1','1')}

@app.route('/')
def hello():
    #Reset choices if not previously reset
    global p1, p2
    if p2 != '':
        print("Reset")
        p1 = ''
        p2 = ''
    return "Hello from Server"

@app.route('/register', methods=["POST"])
def record_decision():
    response = make_response("decision received")
    global p1, p2
    #If prisoner 1 does not already have a decision set their value and cookie
    if p1 == '':
        p1 = request.form['decision']
        response.set_cookie('id', '1')
    #If prisoner 1 has already registered set prisoner 2
    else:
        p2 = request.form['decision']
        response.set_cookie('id', '2')
    return response

#Get the clients cookie and return their reduction
@app.route('/decision')
def determine_reduction():
    if p1 and p2 != '':
        id = request.cookies.get('id')
        key = (p1,p2)
        if id == "1":
            return redux_table.get(key)[0]
        else:
            return redux_table.get(key)[1]
    else:
        return "waiting"

#Randomly decide to award an additional extension
@app.route('/appeal')
def determine_appeal():
    current_reduction = int(request.args.get('input'))
    decision = random.randint(0,1)
    if decision == 1:
        decision = random.randint(1,current_reduction)
        if decision == 1:
            return "Your appeal has been granted and an additional year has been removed"
        else:
            return "Your appeal has been granted and an additional " + str(decision) + " years have been removed"
    else:
        return "Your appeal was denied"

from flask import Flask
from flask import request
import random
import sys
app = Flask(__name__)

#Set the default prisoner 2 choice to C
P2 = 'C'
#The table that determines the sentence reduction based on the prisoner's choices
redux_table = {('C','C'): "5", ('C', 'B'): "2", ('B', 'C'): "3", ('B','B'): "1"}

#Prisoner 2s choice can be set explicity
choice = input("Set prisoner 2's choice to [C] cooperate or [B] betray prisoner 1 (default is [C]): ").upper()
if choice == 'B':
    print("B Chosen")
    P2 = 'B'

#Test the conncetion
@app.route('/')
def hello():
    return "Hello from Server"

#accept the prisoner 1's choice and combine it with prisoner 2 to get the reduction
@app.route('/prosecutor')
def determine_reduction():
    choice = request.args.get('input')
    key = (choice, P2)
    return redux_table.get(key)

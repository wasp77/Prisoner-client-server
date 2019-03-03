import requests
from requests.exceptions import ConnectionError
import textwrap
#Check that a conncetion can be made to the server
#Make sure to add a fail if no server
print("Testing connection...")
try:
    r = requests.get('http://127.0.0.1:5000/')
    print(r.text)

    intro = """You have been chosen to represent a prisoner who was involved in a serious crime with another prisoner.
The prosecutor is trying to decide a sentence for the two prisoners. The prosecutor has given both
prisoners the choice to betray the other by testifying that the other committed the crime or cooperate with
the other by remaining silent."""
    print(textwrap.fill(intro, 75))
    #Get user input for their decision
    choice = input("Please make your choice to [C] cooperate or [B] betray the other prisoner: ").upper()
    print(choice)

    #Loop until they enter a valid choice
    while (choice != 'C' and choice != 'B'):
        choice = input("You have entered an unrecognized value enter [C] to cooperate or [B] to betray: ").upper()

    #Send the choice to the prosecutor endpoint and output the prosecutor's decision
    payload = {'input':choice}
    r = requests.get('http://127.0.0.1:5000/prosecutor', params=payload)
    reduction = int(r.text)
    print("You received a sentence reduction of " + r.text + " years")
except ConnectionError as e:
    print("No connection with the server. Check that server is running.")

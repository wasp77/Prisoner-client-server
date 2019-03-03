import requests
from requests.exceptions import ConnectionError
import time
import textwrap

print("Testing connection...")
try:
    r = requests.get('http://127.0.0.1:5000/')
    print(r.text)

    intro = """You have been chosen to represent a prisoner who was involved in a serious crime with another prisoner.
The prosecutor is trying to decide a sentence for the two prisoners. The prosecutor has given both
prisoners the choice to betray the other by testifying that the other committed the crime or cooperate with
the other by remaining silent."""
    print(textwrap.fill(intro, 75))

    choice = input("Please make your choice to [C] cooperate or [B] betray the other prisoner: ").upper()
    while (choice != 'C' and choice != 'B'):
        choice = input("You have entered an unrecognized value enter [C] to cooperate or [B] to betray: ").upper()

    #Register a decision on the server and save the cookie
    r = requests.post('http://127.0.0.1:5000/register', data={'decision':choice})
    print(r.text)
    cookie = {'id': r.cookies['id']}

    #Poll the server for a decision every second
    while True:
        r = requests.get('http://127.0.0.1:5000/decision', cookies=cookie)
        if r.text != "waiting":
            break
        time.sleep(1)
    reduction = int(r.text)
    print("You received a sentence reduction of " + r.text + " years")

    choice = input("Do you wish to appeal this sentence [Y] yes [N] no: ").upper()
    while (choice != 'Y' and choice != 'N'):
        choice = input("You have entered an unrecognized value enter [Y] yes or [N] no: ").upper()
    #Request an appeal sending the current sentence reduction
    if choice == 'Y':
        payload = {'input':reduction}
        r = requests.get('http://127.0.0.1:5000/appeal', params=payload)
        print(r.text)
except ConnectionError as e:
    print("No connection with the server. Check that server is running.")

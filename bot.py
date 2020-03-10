import requests
import json
from time import sleep

with open("token.txt") as f:
    token = f.readlines()[0]

api_base = "http://diamonds.etimo.se/api"
header = {'Accept':'application/json'}

board_url = api_base + "/Boards"

board = requests.get(url = board_url, headers = header).json()[0]

import requests
import json

api_base = "http://diamonds.etimo.se/api"

bot_dict = {"email":"seallard95@gmail.com", "name":"seal"}
bot_data = json.dumps(bot_dict)
headers = {'Content-type':'application/json', 'Accept':'application/json'}

r = requests.post(api_base + "/Bots", data = bot_data, headers = headers)
data = r.json()

with open("token.txt", "w") as f:
    f.write(data["token"])
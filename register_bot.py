import requests
import json

register_url = "http://diamonds.etimo.se/api/bots"

bot_dict = {"email":"seallard95@gmail.com", "botName":"seal"}
bot_data = json.dumps(bot_dict)
headers = {'Content-type':'application/json', 'Accept':'application/json'}

r = requests.post(register_url, bot_data, headers)
print(r.json())
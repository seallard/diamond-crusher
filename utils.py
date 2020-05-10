import requests
import json
from time import sleep
from time import perf_counter

BOARD_ID = "4"

api_base = "http://diamonds.etimo.se/api"
header = {'Content-Type':'application/json', 'Accept':'application/json'}


def register_bot(email, bot_name):

    register_url = "http://diamonds.etimo.se/api/bots"

    bot_dict = {
    "email": email,
    "botName": bot_name
    }

    bot_data = json.dumps(bot_dict)
    r = requests.post(url=register_url, data=bot_data, headers=header)
    token = r.json()['data']['token']

    return token


def get_distance(location_a, location_b):

    delta_x = location_a['x'] - location_b['x']
    delta_y = location_a['y'] - location_b['y']

    return abs(delta_x) + abs(delta_y)


def get_xy_distance(location_a, location_b):

    delta_x = location_a['x'] - location_b['x']
    delta_y = location_a['y'] - location_b['y']

    return (delta_x, delta_y)


def extract_objects(object_type):

    game_objects = get_game_objects()
    extracted_objects = []

    for game_object in game_objects:
        if game_object['type'] == object_type:
            extracted_objects.append(game_object)

    return extracted_objects


def get_player(player_name):

    bots = extract_objects("BotGameObject")

    for bot in bots:
        if bot['properties']['name'] == player_name:

            return bot


def closest_diamond(player_name):

    diamonds = extract_objects("DiamondGameObject")
    player_position = get_player(player_name)['position']

    shortest_distance = 100
    closest_diamond = None

    for diamond in diamonds:
        diamond_position = diamond['position']

        distance = get_distance(diamond_position, player_position)

        if distance < shortest_distance:
            shortest_distance = distance
            closest_diamond = diamond

    return closest_diamond['position']


def get_direction(xy_distance):

    delta_x, delta_y = xy_distance

    if delta_x < 0:
        return "EAST"

    if delta_x > 0:
        return "WEST"

    if delta_y < 0:
        return "SOUTH"

    if delta_y > 0:
        return "NORTH"


def join_board(token_str):

    join_url = api_base + f"/boards/{BOARD_ID}/join"
    token = json.dumps({"botToken":token_str})
    r = requests.post(url=join_url, data=token, headers=header)

    return r.status_code


def get_game_objects():

    board_url = api_base + f"/boards/{BOARD_ID}"
    board_state = requests.get(board_url, header).json()

    return board_state['data']['gameObjects']


def make_move(direction, token_str):
    """
    Move your piece in the specified direction.
    Assumes board has been joined previously.
    """

    move_url = api_base + f"/boards/{BOARD_ID}/move"
    move = json.dumps({"botToken":token_str, "direction":direction})
    r = requests.post(url = move_url, data = move, headers=header)

    if r.status_code != 200:
        print(f"Move failed: {r.status_code}")

    return r.status_code


def get_minimum_delay():

    data = requests.get(api_base + "/boards").json()['data'][0]
    delay_in_msec = data['minimumDelayBetweenMoves']

    return delay_in_msec/1000


def go_towards(location, delay, player_name, token_str):

    player_location = get_player(player_name)['position']
    xy_distance = get_xy_distance(player_location, location)

    print(f"Distance: {xy_distance}")
    direction = get_direction(xy_distance)

    print(f"Going: {direction}")
    make_move(direction, token_str)
    sleep(delay)


def go_to(position, delay, player_name, token_str):

    player_position = get_player(player_name)['position']

    while player_position != position:

        go_towards(position, delay, player_name, token_str)
        player_position = get_player(player_name)['position']


def number_of_collected_diamonds(player_name):

    return get_player(player_name)['properties']['diamonds']


def get_player_base(name):

    player = get_player(name)
    base = player['properties']['base']

    return base


def find_reset_button():

    reset_button = extract_objects("DiamondButtonGameObject")[0]

    return reset_button['position']
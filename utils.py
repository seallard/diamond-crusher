import requests
import json
from time import sleep
from time import perf_counter
import random

BOARD_ID = "2"

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


def n_closest_diamonds(position, n):

    diamonds = extract_objects("DiamondGameObject")
    closest_diamonds = []

    for diamond in diamonds:

        diamond_position = diamond['position']
        distance = get_distance(diamond_position, position)
        diamond['distance'] = distance
        closest_diamonds.append(diamond)

    closest_diamonds.sort(key=lambda x: x['distance'])

    return closest_diamonds[:n]


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


def make_move(direction, token_str, delay):
    """
    Move your piece in the specified direction.
    Assumes board has been joined previously.
    """

    move_url = api_base + f"/boards/{BOARD_ID}/move"
    move = json.dumps({"botToken":token_str, "direction":direction})
    r = requests.post(url = move_url, data = move, headers=header)

    if r.status_code != 200:
        print(f"Move failed: {r.status_code}")

    sleep(delay)

    return r.status_code


def minimum_delay():

    data = requests.get(api_base + "/boards").json()['data'][0]
    delay_in_msec = data['minimumDelayBetweenMoves']

    return delay_in_msec/1000


def one_way_delay():
    """
    Calculate upper bound for the one-way delay (owd) to the server.
    The processing delay adds some overhead.
    """

    start_time = perf_counter()

    for i in range(5):
        requests.get(api_base)

    stop_time = perf_counter()
    owd = (stop_time - start_time)/10

    return owd


def optimal_delay():

    owd = one_way_delay()
    min_delay = minimum_delay()

    if owd > min_delay:
        return 0

    return min_delay - owd


def handle_illegal_move(direction, token_str, delay):

    directions = ["NORTH", "SOUTH", "WEST", "EAST"]
    directions.remove(direction)
    new_direction = random.choice(directions)

    move_status = make_move(new_direction, token_str, delay)

    return move_status


def go_towards(location, delay, player_name, token_str):

    player_location = get_player(player_name)['position']
    xy_distance = get_xy_distance(player_location, location)

    print(f"Distance: {xy_distance}")
    direction = get_direction(xy_distance)

    print(f"Going: {direction}")
    move_status = make_move(direction, token_str, delay)

    # Handle collisions and other illegal moves
    while move_status != 200:
        move_status = handle_illegal_move(direction, token_str, delay)


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


def average_distance_to_k_diamonds_from_base(base, k):
    """
    Get average distance of the k diamonds closest to
    the collectors base.
    """

    diamonds = n_closest_diamonds(base, k)
    total_distance = sum([diamond['distance'] for diamond in diamonds])

    return total_distance/k


def valid_adjacent_position(position):

    # TODO: make sure position is free (no player base/teleporter)
    if position['x'] < 14:
        position['x'] += 1
        return position

    position['x'] -= 1
    return position


def go_next_to(position, delay, player_name, token_str):

    adjacent = valid_adjacent_position(position)
    go_to(adjacent, delay, player_name, token_str)


def generate_email_addresses(n, base_email):

    emails = []

    for i in range(1, n+1):
        emails.append("."*i + base_email)

    return emails


def generate_bot_names(n, base_name):
    """
    Generates n unique permutations of the base name.
    n must be <= len(base_name)!
    """

    names = set()

    while len(names) < n:
        names.add("".join(random.sample(base_name,len(base_name))))

    return list(names)


def create_bot_army(n, base_email, base_name):

    emails = generate_email_addresses(n, base_email)
    names = generate_bot_names(30, base_name)

    bots = []

    for i, email in enumerate(emails):

        token = register_bot(email, names[i])
        bots.append({'name':names[i], 'token':token})

    with open("bot_army_tokens", 'w') as f:
        json.dump(bots, f)


def read_tokens():

    with open("bot_army_tokens") as f:
        tokens = json.load(f)

    return tokens
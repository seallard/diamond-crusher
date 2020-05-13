import requests
import json
from time import sleep
from time import perf_counter
import random

BOARD_ID = "1"

api_base = "http://diamonds.etimo.se/api"
header = {'Content-Type':'application/json', 'Accept':'application/json'}


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


DELAY = optimal_delay()


def register_bot(email, bot_name):

    register_url = "http://diamonds.etimo.se/api/bots"

    bot_dict = {
    "email": email,
    "botName": bot_name
    }

    bot_data = json.dumps(bot_dict)
    r = requests.post(url=register_url, data=bot_data, headers=header)

    if r.status_code == 200:

        token = r.json()['data']['token']
        return token

    return "invalid"


def get_distance(location_a, location_b):

    delta_x = location_a['x'] - location_b['x']
    delta_y = location_a['y'] - location_b['y']

    return abs(delta_x) + abs(delta_y)


def get_xy_distance(location_a, location_b):

    delta_x = location_a['x'] - location_b['x']
    delta_y = location_a['y'] - location_b['y']

    return (delta_x, delta_y)


def extract_objects(object_type, game_objects):

    extracted_objects = []

    for game_object in game_objects:
        if game_object['type'] == object_type:
            extracted_objects.append(game_object)

    return extracted_objects


def get_player(player_name, objects):

    bots = extract_objects("BotGameObject", objects)

    for bot in bots:
        if bot['properties']['name'] == player_name:

            return bot


def n_closest_diamonds(position, n, objects):

    diamonds = extract_objects("DiamondGameObject", objects)
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
    game_objects = get_game_objects(r.json())

    return game_objects


def get_game_objects(board_state):

    return board_state['data']['gameObjects']


def refresh_game_objects():

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

    sleep(DELAY)

    return r


def handle_illegal_move(direction, token_str):

    directions = ["NORTH", "SOUTH", "WEST", "EAST"]
    directions.remove(direction)

    new_direction = random.choice(directions)
    move = make_move(new_direction, token_str)

    return move


def go_towards(location, player_name, token_str, objects):

    player_location = get_player(player_name, objects)['position']
    xy_distance = get_xy_distance(player_location, location)

    print(f"Distance: {xy_distance}")
    direction = get_direction(xy_distance)

    print(f"Going: {direction}")
    move = make_move(direction, token_str)

    # Handle collisions and other illegal moves
    while move.status_code != 200:
        move = handle_illegal_move(direction, token_str)

    game_objects = get_game_objects(move.json())

    return game_objects


def go_to(position, player_name, token_str, objects):

    player_position = get_player(player_name, objects)['position']

    while player_position != position:

        objects = go_towards(position, player_name, token_str, objects)
        player_position = get_player(player_name, objects)['position']

    return objects


def number_of_collected_diamonds(player_name, objects):

    return get_player(player_name, objects)['properties']['diamonds']


def get_player_base(name, objects):

    player = get_player(name, objects)
    base = player['properties']['base']

    return base


def find_reset_button(objects):

    reset_button = extract_objects("DiamondButtonGameObject", objects)[0]

    return reset_button['position']


def average_distance_to_k_diamonds_from_position(position, k, objects):
    """
    Get average distance of the k diamonds closest to the position.
    """

    diamonds = n_closest_diamonds(position, k, objects)
    total_distance = sum([diamond['distance'] for diamond in diamonds])

    return total_distance/k


def valid_adjacent_position(position):

    # TODO: make sure position is free (no player base/teleporter)
    if position['x'] < 14:
        position['x'] += 1
        return position

    position['x'] -= 1
    return position


def go_next_to(position, player_name, token_str, objects):

    adjacent = valid_adjacent_position(position)
    game_objects = go_to(adjacent, player_name, token_str, objects)

    return game_objects




def generate_email_addresses(n, base_email):
    """
    n must be smaller than 5! and the first part of the
    gmail address must be longer than 6 chars.
    """

    emails = set()
    permute_part = base_email[:6]

    while len(emails) < n:
        number_of_periods = random.randrange(1, len(permute_part)-1)
        indices = random.sample(range(1, len(permute_part)), number_of_periods)
        indices.sort()

        parts = []
        previous_index = 0

        for index in indices:
            parts.append(base_email[previous_index:index] + ".")
            previous_index = index

        parts.append(base_email[previous_index:])
        permutated_email = "".join(parts)

        emails.add(permutated_email)

    return list(emails)


def generate_bot_names(n, base_name):
    """
    Generates n unique permutations of the base name.
    n must be <= len(base_name)!
    """

    names = set()

    while len(names) < n:
        names.add("".join(random.sample(base_name,len(base_name))))

    return list(names)


def create_bot_army(n, base_email, base_name, file_name):

    emails = generate_email_addresses(n, base_email)
    names = generate_bot_names(n, base_name)

    bots = []

    for i, email in enumerate(emails):

        token = register_bot(email, names[i])
        bots.append({'name':names[i], 'token':token})

    with open(file_name, 'w') as f:
        json.dump(bots, f)


def read_tokens(file_name):

    with open(file_name) as f:
        tokens = json.load(f)

    return tokens


def join_with_optimal_position(tokens_file_name):
    """
    Spawn collector in the center of the board.
    """
    bots = read_tokens("tokens/collector_tokens")

    pass


def closest_border(position):
    """
    Find closest border position and return location.
    Board dimensions are hard coded.
    """

    width = 14
    height = 14

    x = position['x']
    y = position['y']

    # Distances to border in each direction
    east = (width - x, {'x':width, 'y':y})
    west = (x, {'x':0, 'y':y})
    north = (y, {'x':x, 'y':0})
    south = (height-y, {'x':x, 'y':14})

    distances = [east, west, north, south]
    closest_location = min(distances, key = lambda t: t[0])

    return closest_location(1)


def spawn_and_place_gargoyle(token, name):

    join_board(token)
    make_move("NORTH", token)

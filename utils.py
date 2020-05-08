import requests
import json
from time import sleep
from time import perf_counter

BOARD_ID = "4"

api_base = "http://diamonds.etimo.se/api"
header = {'Content-Type':'application/json', 'Accept':'application/json'}


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


def join_board(token):

    join_url = api_base + f"/boards/{BOARD_ID}/join"
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


def calculate_server_latency():
    """
    Ping API and measure latency in seconds.
    Calculated as the average of 5 consecutive pings.
    """

    start_time = perf_counter()

    for i in range(5):
        requests.get(api_base)

    stop_time = perf_counter()
    average_latency = (stop_time - start_time)/5

    return average_latency


def get_minimum_delay():

    data = requests.get(api_base + "/boards").json()['data'][0]
    delay_in_msec = data['minimumDelayBetweenMoves']

    return delay_in_msec/1000


def calculate_optimal_sleep():
    """
    Determine optimal sleep period between calls to the API.
    """

    average_latency = calculate_server_latency()
    minimum_delay = get_minimum_delay()
    optimal_delay = minimum_delay-(average_latency/2)

    if optimal_delay < 0:
        return 0

    return optimal_delay


def go_towards(location, delay, player_name, token_str):

    player_location = get_player(player_name)['position']
    xy_distance = get_xy_distance(player_location, location)

    print(f"Distance: {xy_distance}")
    direction = get_direction(xy_distance)

    print(f"Going: {direction}")
    make_move(direction, token_str)
    sleep(delay)


def number_of_collected_diamonds(player_name):

    return get_player(player_name)['properties']['diamonds']


def get_player_base(name):

    player = get_player(name)
    base = player['properties']['base']

    return base
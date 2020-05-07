import requests
import json
from time import sleep
from time import perf_counter
import networkx as nx


with open("token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})


api_base = "http://diamonds.etimo.se/api"
header = {'Content-Type':'application/json', 'Accept':'application/json'}

PLAYER = "seal"
BOARD_ID = "2"


def join_board():

    join_url = api_base + f"/boards/{BOARD_ID}/join"
    r = requests.post(url=join_url, data=token, headers=header)

    return r.status_code


def get_game_objects():

    board_url = api_base + f"/boards/{BOARD_ID}"
    board_state = requests.get(board_url, header).json()

    return board_state['data']['gameObjects']


def make_move(direction):
    """
    Move your piece in the specified direction.
    Assumes board has been joined previously.
    """

    move_url = api_base + f"/boards/{BOARD_ID}/move"
    move = json.dumps({"botToken":token_str, "direction":direction})
    r = requests.post(url = move_url, data = move, headers=header)

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

    optimal_delay = minimum_delay-average_latency

    if optimal_delay < 0:
        return 0

    return optimal_delay


def get_distance(location_a, location_b):

    delta_x = location_a['x'] - location_b['x']
    delta_y = location_a['y'] - location_b['y']

    return abs(delta_x) + abs(delta_y)


def get_xy_distance(location_a, location_b):

    delta_x = location_a['x'] - location_b['x']
    delta_y = location_a['y'] - location_b['y']

    return (delta_x, delta_y)


def extract_object(object_type, game_objects):

    objects = []

    for game_object in game_objects:
        if game_object['type'] == object_type:
            objects.append(game_object)

    return objects


def extract_player_object(game_objects):

    bots = extract_object("BotGameObject", game_objects)

    for bot in bots:
        if bot['properties']['name'] == PLAYER:

            return bot


def closest_diamond(game_objects):

    diamonds = extract_object("DiamondGameObject", game_objects)
    player_position = extract_player_object(game_objects)['position']

    shortest_distance = 100
    closest_diamond = None

    for diamond in diamonds:
        diamond_position = diamond['position']

        distance = get_distance(diamond_position, player_position)

        if distance < shortest_distance:
            shortest_distance = distance
            closest_diamond = diamond

    return closest_diamond['position']


def generate_path(xy_distance):

    delta_x, delta_y = xy_distance
    path = []

    if delta_x < 0:
        [path.append("EAST") for x in range(abs(delta_x))]

    else:
        [path.append("WEST") for x in range(delta_x)]

    if delta_y < 0:
        [path.append("SOUTH") for y in range(abs(delta_y))]

    else:
        [path.append("NORTH") for y in range(delta_y)]

    return path


def go_to(location, game_objects, delay):

    player_location = extract_player_object(game_objects)['position']
    print(f"Player location: {player_location}")
    xy_distance = get_xy_distance(player_location, location)
    print(f"xy distance: {xy_distance}")
    path = generate_path(xy_distance)
    print(f"Generated path: {path}")

    for step in path:
        move_status = make_move(step)
        print(f"Move status: {move_status}")
        sleep(0.1)


def main():

    delay = calculate_optimal_sleep()
    join_board()
    objects = get_game_objects()

    # Find location of closest diamond
    diamond_location = closest_diamond(objects)
    go_to(diamond_location, objects, delay)



if __name__ == "__main__":
    main()
import requests
import json
from time import sleep
from time import perf_counter

with open("token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})

api_base = "http://diamonds.etimo.se/api"
header = {'Content-Type':'application/json', 'Accept':'application/json'}


def join_board(board_id):

    join_url = api_base + f"/boards/{board_id}/join"
    r = requests.post(url=join_url, data=token, headers=header)
    return r.status_code


def get_board_state(board_id):

    board_url = api_base + f"/boards/{board_id}"
    board_info = requests.get(board_url, header).json()
    return board_info


def make_move(board_id, direction):
    """
    Move your piece in the specified direction.
    Assumes board has been joined previously.
    """

    move_url = api_base + f"/boards/{board_id}/move"
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

    return minimum_delay-average_latency


def find_closest_diamond():
    pass


def main():

    delay = calculate_optimal_sleep()

    join_board("1")
    data = get_board_state("1")
    make_move("1", "EAST")


if __name__ == "__main__":
    main()
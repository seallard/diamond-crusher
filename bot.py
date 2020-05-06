import requests
import json
from time import sleep

with open("token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})

api_base = "http://diamonds.etimo.se/api"
header = {'Content-Type':'application/json', 'Accept':'application/json'}


def join_board(board_id):

    join_url = api_base + f"/boards/{board_id}" + "/join"
    r = requests.post(url=join_url, data=token, headers=header)
    return r.status_code


def get_board_state(board_id):

    board_url = api_base + f"/boards/{board_id}"
    board_info = requests.get(board_url, header).json()
    return board_info


def make_move(board_id, direction):

    move_url = api_base + f"/boards/{board_id}/move"
    move = json.dumps({"botToken":token_str, "direction":direction})
    r = requests.post(url = move_url, data = move, headers=header)
    return r.status_code


def find_closest_diamond():
    pass


def main():
    join_board("1")
    data = get_board_state("1")
    make_move("1", "EAST")


if __name__ == "__main__":
    main()
from utils import *


bot_name = "jarvis"

with open("tokens/replenisher_token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})


def main():

    join_board(token)
    base = get_player_base(bot_name)
    delay = calculate_optimal_sleep()

    while True:

        pass


if __name__ == "__main__":
    main()
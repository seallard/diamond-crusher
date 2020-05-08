from utils import *


bot_name = "seal"

with open("tokens/collector_token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})


def main():

    join_board(token)
    base = get_player_base(bot_name)
    delay = calculate_optimal_sleep()

    while True:

        collected_diamonds = 0

        while collected_diamonds < 4:

            diamond = closest_diamond(bot_name)
            go_towards(diamond, delay, bot_name, token_str)
            collected_diamonds = number_of_collected_diamonds(bot_name)

        go_towards(base, delay, bot_name, token_str)


if __name__ == "__main__":
    main()
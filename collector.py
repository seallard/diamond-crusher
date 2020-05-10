from utils import *


bot_name = "seal"

with open("tokens/collector_token.txt") as f:
    token_str = f.readlines()[0].rstrip()


def main():

    join_board(token_str)
    base = get_player_base(bot_name)
    delay = 0.1

    while True:

        collected_diamonds = 0

        while collected_diamonds < 4:

            diamond = closest_diamond(bot_name)
            go_towards(diamond, delay, bot_name, token_str)
            collected_diamonds = number_of_collected_diamonds(bot_name)

        go_to(base, delay, bot_name, token_str)


if __name__ == "__main__":
    main()
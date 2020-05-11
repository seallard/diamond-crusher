from utils import *


bot_name = "seal"

with open("tokens/collector_token.txt") as f:
    token_str = f.readlines()[0].rstrip()


def main():

    join_board(token_str)
    base = get_player_base(bot_name)
    delay = optimal_delay()

    while True:

        collected_diamonds = 0

        while collected_diamonds < 5:

            diamond = n_closest_diamonds(base, 1)[0]
            diamond_value = diamond['properties']['points']

            if diamond_value + collected_diamonds > 5:
                break

            go_towards(diamond['position'], delay, bot_name, token_str)
            collected_diamonds = number_of_collected_diamonds(bot_name)

        go_to(base, delay, bot_name, token_str)


if __name__ == "__main__":
    main()
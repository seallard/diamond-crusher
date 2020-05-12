from utils import *


bot_name = "seal"

token_str = "faf07104-563d-4702-82c6-784ff9694a24"

def main():

    join_board(token_str)
    base = get_player_base(bot_name)

    while True:

        collected_diamonds = 0

        while collected_diamonds < 5:

            diamond = n_closest_diamonds(base, 1)[0]
            diamond_value = diamond['properties']['points']

            if diamond_value + collected_diamonds > 5:
                break

            go_towards(diamond['position'], bot_name, token_str)
            collected_diamonds = number_of_collected_diamonds(bot_name)

        go_to(base, bot_name, token_str)


if __name__ == "__main__":
    main()
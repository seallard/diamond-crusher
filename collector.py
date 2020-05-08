from utils import *


name = "seal"

def main():

    delay = calculate_optimal_sleep()
    join_board()

    while True:

        player = get_player(name)
        base = player['properties']['base']
        collected_diamonds = 0

        while collected_diamonds < 4:

            diamond = closest_diamond(name)
            go_towards(diamond, delay, name)
            collected_diamonds = number_of_collected_diamonds(name)

        go_towards(base, delay, name)


if __name__ == "__main__":
    main()
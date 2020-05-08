from utils import *


name = "seal"

def main():

    join_board()
    base = get_player_base(name)
    delay = calculate_optimal_sleep()

    while True:

        collected_diamonds = 0

        while collected_diamonds < 4:

            diamond = closest_diamond(name)
            go_towards(diamond, delay, name)
            collected_diamonds = number_of_collected_diamonds(name)

        go_towards(base, delay, name)


if __name__ == "__main__":
    main()
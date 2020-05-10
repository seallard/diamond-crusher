from utils import *


bot_name = "jarvis"

with open("tokens/replenisher_token.txt") as f:
    token_str = f.readlines()[0].rstrip()


def main():

    join_board(token_str)
    delay = optimal_delay()
    threshold = 7

    while True:

        while average_distance_to_diamond_from_base("seal") < threshold:
            sleep(0.5)

        reset_button = find_reset_button()
        go_to(reset_button, delay, bot_name, token_str)


if __name__ == "__main__":
    main()
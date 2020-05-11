from utils import *


bot_name = "jarvis"

with open("tokens/replenisher_token.txt") as f:
    token_str = f.readlines()[0].rstrip()


def main():

    join_board(token_str)
    delay = optimal_delay()

    reset_button = find_reset_button()
    go_next_to(reset_button, delay, bot_name, token_str)
    base = get_player_base("seal")

    threshold = 6

    while True:

        reset_button = find_reset_button()
        go_next_to(reset_button, delay, bot_name, token_str)

        while average_distance_to_k_diamonds_from_base(base, 5) < threshold and number_of_collected_diamonds("seal") < 5:
            sleep(0.1)

        # The collector might have reset the board by accident
        reset_button = find_reset_button()
        go_to(reset_button, delay, bot_name, token_str)


if __name__ == "__main__":
    main()
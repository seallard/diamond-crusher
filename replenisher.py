from utils import *


bot_name = "jarvis"

with open("tokens/replenisher_token.txt") as f:
    token_str = f.readlines()[0].rstrip()


def main():

    objects = join_board(token_str)

    reset_button = find_reset_button(objects)
    go_next_to(reset_button, bot_name, token_str, objects)
    base = get_player_base("seal", objects)

    threshold = 6

    while True:

        reset_button = find_reset_button(objects)
        objects = go_next_to(reset_button, bot_name, token_str, objects)

        while average_distance_to_k_diamonds_from_position(base, 5, objects) < threshold and number_of_collected_diamonds("seal", objects) < 5:
            objects = refresh_game_objects()
            sleep(0.5)

        # The collector might have reset the board by accident
        reset_button = find_reset_button(objects)
        go_to(reset_button, bot_name, token_str, objects)


if __name__ == "__main__":
    main()
from utils import *


bot = "jarvis"
collector = "seal"
token_str = "0289b2f8-6255-407d-8d21-834474792381"

def main():

    join_board(token_str)

    while True:
        objects = refresh_game_objects()
        reset_button = find_reset_button(objects)
        go_next_to(reset_button, bot, token_str, objects)

        while worth_hunting(collector):
            objects = refresh_game_objects()
            check_reset = find_reset_button(objects)

            if check_reset != reset_button:
                reset_button = check_reset
                go_next_to(reset_button, bot, token_str, objects)

        go_to(reset_button, bot, token_str, objects)


if __name__ == "__main__":
    main()
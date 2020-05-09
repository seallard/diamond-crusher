from utils import *


bot_name = "jarvis"

with open("tokens/replenisher_token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})


def main():

    join_board(token)
    delay = 0.1

    while True:

        reset_button = find_reset_button()
        go_to(reset_button, delay, bot_name, token_str)

        # monitor diamond concentration around collectors home
        # step on button when below threshold
        pass


if __name__ == "__main__":
    main()
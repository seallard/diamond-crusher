from utils import *


bot_name = "jarvis"

with open("tokens/replenisher_token.txt") as f:
    token_str = f.readlines()[0]
    token = json.dumps({"botToken":token_str})


def main():

    join_board(token)
    delay = calculate_optimal_sleep()

    while True:

        reset_button = find_reset_button()

        # go to reset button
        # monitor diamond concentration around collectors home
        # step on button when below threshold
        pass


if __name__ == "__main__":
    main()
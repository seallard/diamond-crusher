from utils import *

bot = "seal"
token_str = "151bd1b1-81fb-414b-aebc-055a42750bad"

def main():

    join_board(token_str)
    objects = refresh_game_objects()
    base = get_player_base(bot, objects)

    while True:

        while worth_hunting(bot):

            diamond = n_closest_diamonds(base, 1, objects)[0]['position']
            objects = go_towards(diamond, bot, token_str)

        objects = go_to(base, bot, token_str, objects)


if __name__ == "__main__":
    main()
from utils import *
import threading

bot, token = join_with_optimal_position("tokens/test_tokens")
t = threading.Thread(target = spawn_replenisher, args=(bot,))
t.start()

def main():

    join_board(token)
    objects = refresh_game_objects()
    base = get_player_base(bot, objects)

    while True:

        while worth_hunting(bot):

            diamond = best_diamond(bot, objects)
            objects = go_to(diamond, bot, token, objects)

        objects = go_to(base, bot, token, objects)


if __name__ == "__main__":
    main()
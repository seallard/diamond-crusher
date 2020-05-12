from utils import *
import threading


bots = read_tokens("tokens/gargoyle_tokens")
positions = get_gargoyle_positions()

def main():

    for i, gargoyle in enumerate(bots):

        token = gargoyle['token']
        name = gargoyle['name']
        position = positions[i]

        t = threading.Thread(target = spawn_and_place_gargoyle, args=(token, name, position))
        t.start()

main()
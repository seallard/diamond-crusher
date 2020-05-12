from utils import *
import threading


bots = read_tokens("tokens/gargoyle_tokens")

def main():

    for gargoyle in bots:

        token = gargoyle['token']
        t = threading.Thread(target = spawn_and_place_gargoyle, args=(token,))
        t.start()

main()
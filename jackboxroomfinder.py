import argparse
import json
import string
import requests
import signal
import sys
import time
from multiprocessing import Pool
from itertools import product

urlBase = "https://ecast.jackboxgames.com/api/v2/rooms/"
defaultNumThreads = 50

# parse options
parser = argparse.ArgumentParser(description="Find every jackbox room currently open.")

parser.add_argument("-q", "--quiplash", help="show only quiplash games", action="store_true")
parser.add_argument("-t", "--numthreads", default=defaultNumThreads, type=int, help="number of therads to use when going through the possible rooms")
parser.add_argument("-n", "--numrequests", default=10000, type=int, help="number of requests to run before quitting. Max is 456976")

lockGroup = parser.add_mutually_exclusive_group()
lockGroup.add_argument("-l", "--locked", help="only show locked games", action="store_true")
lockGroup.add_argument("-L", "--notlocked", help="only show games that are not locked", action="store_true")
fullGroup = parser.add_mutually_exclusive_group()
fullGroup.add_argument("-f", "--full", help="only show full games", action="store_true")
fullGroup.add_argument("-F", "--notfull", help="only show games that are not full", action="store_true")
audienceGroup = parser.add_mutually_exclusive_group()
audienceGroup.add_argument("-a", "--audience", help="only show games that allow an audience", action="store_true")
audienceGroup.add_argument("-A", "--notaudience", help="only show games that do not allow an audience", action="store_true")
moderationGroup = parser.add_mutually_exclusive_group()
moderationGroup.add_argument("-m", "--moderated", help="only show moterated games", action="store_true")
moderationGroup.add_argument("-M", "--notmoderated", help="only show games that are not moterated", action="store_true")

args = parser.parse_args()

if args.numrequests < 0 or args.numrequests > 456976:
    print("Input error. Num requests must be positive int below 456976 Exiting.", file=sys.stderr)
    sys.exit(1)

def generateRoomCodes(length):
    """
    Return list with all possible room codes
    """
    chars = string.ascii_uppercase
    code_list = [''.join(i) for i in product(chars, repeat=length)]
    return code_list

def threadGetRoom(roomCode):
    """
    Takes a room code and makes a request. If it comes back good, print it.
    """
    r = requests.get(urlBase + roomCode)
    if r.status_code != 404:
        body = json.loads(r.text)['body']

        appTag = body['appTag']
        locked = 'Y' if body['locked'] == True else 'N'
        full = 'Y' if body['full'] == True else 'N'
        audience = 'Y' if body['audienceEnabled'] == True else 'N'
        moderation = 'Y' if body['moderationEnabled'] == True else 'N'

        # run down requirements and see if it can be printed
        toPrint = True

        if body['passwordRequired'] == True:
            toPrint = False
        if args.quiplash and 'quiplash' not in appTag:
            toPrint = False
        if (args.locked and locked == 'N') or (args.notlocked and locked == 'Y'):
            toPrint = False
        if (args.full and full == 'N') or (args.notfull and full == 'Y'):
            toPrint = False
        if (args.audience and audience == 'N') or (args.notaudience and audience == 'Y'):
            toPrint = False
        if (args.moderated and moderation == 'N') or (args.notmoderated and moderation == 'Y'):
            toPrint = False

        if toPrint:
            print("""|   %4s    | %-20s |    %1s    |   %1s   |     %1s     |      %1s      |
+-----------+----------------------+---------+-------+-----------+-------------+""" 
                    % (roomCode, appTag, locked, full, audience, moderation))


def getRooms():
    """
    Main function. manages threads.
    """
    startTime = time.time()
    roomCodes = generateRoomCodes(4)[:args.numrequests]

    # put room codes into a queue
    with Pool(args.numthreads) as p:
        p.map(threadGetRoom, roomCodes)

    endTime = time.time()
    print("Ran %d requests in %f seconds" % (args.numrequests, endTime - startTime))


if __name__ == "__main__":
    print("""
Getting All Jackbox Rooms:
+-----------+----------------------+---------+-------+-----------+-------------+
| Room Code |         Game         | Locked? | Full? | Audience? | Moderation? |
+-----------+----------------------+---------+-------+-----------+-------------+""")
    getRooms()


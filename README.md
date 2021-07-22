# jackbox-room-finder
Finds open Jackbox rooms through their API.

Dependencies:
	- requests. Install with `pip install requests`

Usage: Clone and run with these options.

```
usage: jackboxroomfinder.py [-h] [-q] [-t NUMTHREADS] [-n NUMREQUESTS] [-l | -L] [-f | -F] [-a | -A] [-m | -M]

Find every jackbox room currently open.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiplash        show only quiplash games
  -t NUMTHREADS, --numthreads NUMTHREADS
                        number of therads to use when going through the possible rooms
  -n NUMREQUESTS, --numrequests NUMREQUESTS
                        number of requests to run before quitting. Max is 456976
  -l, --locked          only show locked games
  -L, --notlocked       only show games that are not locked
  -f, --full            only show full games
  -F, --notfull         only show games that are not full
  -a, --audience        only show games that allow an audience
  -A, --notaudience     only show games that do not allow an audience
  -m, --moderated       only show moterated games
  -M, --notmoderated    only show games that are not moterated
```

Enjoy and be nice lol.
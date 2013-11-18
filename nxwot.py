import bz2
import sys


if len(sys.argv) < 2:
    sys.stderr.write("nxwot.py <WOT file>\n")
    sys.exit(1)


filename = sys.argv[1]

print(bz2.BZ2File(filename))

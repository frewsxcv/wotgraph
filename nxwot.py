import bz2
import sys

def parse_nodes(g, keysfile, namesfile):
    while True:
        g.add_node(keyid, name=name)

def parse_edges(g, sigfile):
    raise NotImplementedError

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("nxwot.py <WOT file>\n")
        sys.exit(1)


    filename = sys.argv[1]

    print(bz2.BZ2File(filename))

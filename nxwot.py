import bz2
import sys
import networkx as nx

def read_wot(keysfile, namesfile, sigsfile):
    G = nx.MultiDiGraph()

    while True:
        keysfile.read(4)
        name = namesfile.readline()
        if not keyid or not name:
            break
        G.add_node(keyid, name=name)

    while False:
        G.add_edge(signer, owner)

    return G

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("nxwot.py <WOT file>\n")
        sys.exit(1)


    filename = sys.argv[1]

    print(bz2.BZ2File(filename))

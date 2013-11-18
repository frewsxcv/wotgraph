import bz2
import sys
import networkx as nx

def read_nodes(G, keysfile, namesfile):
    while True:
        G.add_node(keyid, name=name)

def read_edges(G, sigsfile):
    raise NotImplementedError

def read_graph(keysfile, namesfile, sigsfile):
    G = nx.MultiDiGraph()
    read_nodes(G, keysfile, namesfile)
    read_edges(G, sigsfile)
    return G

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("nxwot.py <WOT file>\n")
        sys.exit(1)


    filename = sys.argv[1]

    print(bz2.BZ2File(filename))

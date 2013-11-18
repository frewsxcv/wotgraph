import bz2
import sys
import networkx as nx
import arpy

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


def get_files(wot_filename):
    wot_files = {}

    with bz2.BZ2File(wot_filename) as wot_ar:
        wot_archive = arpy.Archive(fileobj=wot_ar)
        for f in wot_archive:
            filename = f.header.name.decode()
            wot_files[filename] = f.read()

    return wot_files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("nxwot.py <WOT file>\n")
        sys.exit(1)

    filename = sys.argv[1]
    files = get_files(filename)

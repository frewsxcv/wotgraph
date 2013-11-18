import bz2
import io
import sys
import urllib.request
import networkx as nx
import arpy

def read_wot(keysfile, namesfile, sigsfile):
    G = nx.MultiDiGraph()

    names = namesfile.split("\n")
    keys = [int.from_bytes(keysfile[i:i+4], byteorder='big')
            for i in range(0, len(keysfile), 4)]
    for n, k in zip(names, keys):
        G.add_node(k, name=n)

    #G.add_edge(signer, owner)

    return G


def latest_wot():
    url = "http://wot.christoph-egger.org/download/latest.wot"
    return urllib.request.urlopen(url)


def get_files(wot_file):
    wot_files = {}

    with bz2.BZ2File(wot_file) as wot_ar:
        wot_archive = arpy.Archive(fileobj=wot_ar)
        for f in wot_archive:
            filename = f.header.name.decode()
            wot_files[filename] = f.read()

    return wot_files

if __name__ == "__main__":

    if len(sys.argv) < 2:
        wot_file = latest_wot()
    else:
        filename = sys.argv[1]
        wot_file = open(filename, "rb")

    files = get_files(wot_file)

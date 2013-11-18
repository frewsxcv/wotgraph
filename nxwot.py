import bz2
import io
import sys
import urllib.request
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

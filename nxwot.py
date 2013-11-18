import bz2
import io
import sys
import urllib.request
import networkx as nx
import arpy

def read_wot(keysfile, namesfile, sigsfile):
    G = nx.MultiDiGraph()

    keys = list()
    while True:
        name = namesfile.readline()
        if not name:
            break

        keyid = int.from_bytes(keysfile.read(4), byteorder='big')
        keys.append(keyid)
        G.add_node(keyid, name=name)

        numsigs = int.from_bytes(sigsfile.read(4), byteorder='big')
        for i in range(numsigs):
            signer_index = int.from_bytes(sigsfile.read(4), byteorder='big')
            signer_index = signer_index & 0x0FFFFFFF
            signer = keys[signer_index]
            G.add_edge(signer, keyid)


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
            contents = io.BytesIO(f.read())
            wot_files[filename] = contents

    return wot_files

if __name__ == "__main__":

    if len(sys.argv) < 2:
        wot_file = latest_wot()
    else:
        filename = sys.argv[1]
        wot_file = open(filename, "rb")

    files = get_files(wot_file)

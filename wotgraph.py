#!/usr/bin/env python3

import argparse
import bz2
import io
import sys
import urllib.request

import networkx as nx
import arpy


def read_wot(keysfile, namesfile, sigsfile):
    G = nx.DiGraph()

    keys = list()
    for name in namesfile:
        keyid = int.from_bytes(keysfile.read(4), byteorder="big")
        keyid = "{0:X}".format(keyid)
        keys.append(keyid)
        name = name.decode("utf-8", errors="replace").strip()
        G.add_node(keyid, label=name)

    for owner in keys:
        numsigs = int.from_bytes(sigsfile.read(4), byteorder="big")
        for i in range(numsigs):
            sig_info = int.from_bytes(sigsfile.read(4), byteorder="big")
            signer = keys[sig_info & 0x0FFFFFFF]
            primary = sig_info & 0x40000000 == 0x40000000
            level = (sig_info & 0x30000000) >> 28
            G.add_edge(signer, owner, primary_id=primary, cert_level=level)

    return G


def latest_wot():
    url = "http://wot.christoph-egger.org/download/latest.wot"
    return urllib.request.urlopen(url)


def extract_wot(wot_file):
    wot_files = {}

    with bz2.BZ2File(wot_file) as wot_ar:
        wot_archive = arpy.Archive(fileobj=wot_ar)
        for f in wot_archive:
            filename = f.header.name.decode()
            contents = io.BytesIO(f.read())
            wot_files[filename] = contents

    return wot_files

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate web of trust graph")
    parser.add_argument(
        "-w", "--wot",
        dest="wot_filename",
        help="use local .wot file",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["gexf", "graphml", "yaml"],
        dest="file_format",
        default="gexf",
        help="specify file format of outputted graph",
    )
    parser.add_argument(
        "-o", "--output",
        help="output filename",
    )
    args = parser.parse_args()

    if args.wot_filename:
        wot_file = open(args.wot_filename, "rb")
    else:
        wot_file = latest_wot()

    files = extract_wot(wot_file)

    G = read_wot(files["keys"], files["names"], files["signatures"])

    if args.output:
        outfile = open(args.output, "wb")
    else:
        outfile = sys.stdout.buffer

    if args.file_format == "gexf":
        nx.write_gexf(G, outfile)
    elif args.file_format == "graphml":
        nx.write_graphml(G, outfile)
    elif args.file_format == "yaml":
        nx.write_yaml(G, outfile)

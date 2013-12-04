#!/usr/bin/env python3

"""
This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain
one at http://mozilla.org/MPL/2.0/.
"""

import argparse
import bz2
import io
import sys
import urllib2
import logging
import struct

import networkx as nx
import arpy


def read_wot(wot_file):

    def read_int32(f):
        return struct.unpack(">L", f.read(4))[0]

    files = {}

    decompressed = bz2.decompress(wot_file.read())
    extracted = arpy.Archive(fileobj=io.BytesIO(decompressed))
    for file_ in extracted:
        filename = file_.header.name.decode()
        contents = io.BytesIO(file_.read())
        files[filename] = contents

    G = nx.DiGraph()

    keys = list()
    for name in files["names"]:
        keyid = read_int32(files["keys"])
        keyid = "{0:08X}".format(keyid)
        keys.append(keyid)
        name = name.decode("utf-8", errors="replace").strip()
        G.add_node(keyid, label=name)
        logging.debug("pub {0}".format(keyid))

    for owner in keys:
        numsigs = read_int32(files["signatures"])
        for i in range(numsigs):
            sig_info = read_int32(files["signatures"])
            signer = keys[sig_info & 0x0FFFFFFF]
            primary = sig_info & 0x40000000 == 0x40000000
            level = (sig_info & 0x30000000) >> 28
            logging.debug("sig by {0} on {1}".format(signer, owner))
            G.add_edge(signer, owner, primary_id=primary, cert_level=level)

    return G


def latest_wot():
    logging.info("Retrieving wot file...")
    url = "http://wot.christoph-egger.org/download/latest.wot"
    return urllib2.urlopen(url)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate web of trust graph")
    parser.add_argument(
        "wot_file",
        nargs="?",
        help=".wot file",
    )
    parser.add_argument(
        "-k", "--key",
        type=str.upper,
        help="central key for ego network",
    )
    parser.add_argument(
        "-r", "--radius",
        default=3,
        type=int,
        help="radius of ego network",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["gexf", "graphml", "yaml"],
        dest="file_format",
        default="gexf",
        help="specify file format of outputted graph",
    )
    parser.add_argument(
        "-s", "--save",
        action="store_true",
        help="download latest .wot file to given filename",
    )
    parser.add_argument(
        "-o", "--output",
        help="output filename",
    )
    parser.add_argument(
        "-m", "--mutual",
        action="store_true",
        help="only keep mutually signed signatures",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="print progress information",
    )
    args = parser.parse_args()

    logging.basicConfig(format="%(levelname)s: %(message)s",
                        level=['WARNING', 'INFO', 'DEBUG'][args.verbose])

    if args.wot_file:
        if args.save:
            wot_file = open(args.wot_file, "w+b")
            wot_file.write(latest_wot().read())
            wot_file.seek(0)
        else:
            wot_file = open(args.wot_file, "rb")
    else:
        wot_file = latest_wot()

    logging.info("Parsing files...")
    G = read_wot(wot_file)
    logging.info("Read {0} keys, {1} signatures".format(nx.number_of_nodes(G),
                                                        nx.number_of_edges(G)))

    logging.info("Filtering...")
    if args.mutual:
        G = G.to_undirected(reciprocal=True)
        G = nx.connected_component_subgraphs(G)[0]

    if args.key:
        G = nx.ego_graph(G, args.key, radius=args.radius, undirected=True)

    logging.info("Writing output file...")
    if args.output:
        outfile = open(args.output, "wb")
    else:
        outfile = sys.stdout

    if args.file_format == "gexf":
        nx.write_gexf(G, outfile)
    elif args.file_format == "graphml":
        nx.write_graphml(G, outfile)
    elif args.file_format == "yaml":
        nx.write_yaml(G, outfile)

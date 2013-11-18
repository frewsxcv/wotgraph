import bz2
import sys

import arpy


def get_files(wot_filename):
    with bz2.BZ2File(wot_filename) as wot_ar:
        wot_archive = arpy.Archive(fileobj=wot_ar)
        wot_files = {}

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

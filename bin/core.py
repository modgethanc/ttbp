#!/usr/bin/python

import os

WWW = os.path.join("..","www")
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")

HEADER = open(os.path.join(CONFIG, "header.txt")).read()
FOOTER = open(os.path.join(CONFIG, "footer.txt")).read()

FILES = []

for file in os.listdir(DATA):
    filename = os.path.join(DATA, file)
    if os.path.isfile(filename) and os.path.splitext(filename)[1] == ".txt":
        FILES.append(file)

print FILES

def write(outurl="default.html"):
    outfile = open(os.path.join(WWW, outurl), "w")

    for line in HEADER:
        outfile.write(line)

    #for line in write_placeholder():
    #    outfile.write(line)

    for file in FILES:
        for line in write_entry(file):
            outfile.write(line)

    for line in FOOTER:
        outfile.write(line)

    outfile.close()

def write_entry(file):
    # dump given file into entry format, return as list of strings

    date = parse_date(file)

    entry = [
        "\t\t<p><a name=\""+date[0]+date[1]+date[2]+"\"></a><br /><br /></p>\n",
        "\t\t<div class=\"entry\">\n",
        "\t\t\t<h5><a href=\"#"+date[0]+date[1]+date[2]+"\">"+date[2]+"</a> month "+date[0]+"</h5>\n",
        "\t\t\t<P>"
    ]

    raw = []
    rawfile = open(os.path.join(DATA, file), "r")

    for line in rawfile:
        raw.append(line)
    rawfile.close()

    print raw

    for line in raw:
        entry.append(line+"\t\t\t")
        if line == "\n":
            entry.append("</p>\n\t\t\t<p>")

    entry.append("</p>\n\t\t</div>\n")

    return entry

def parse_date(file):
    # assuming a filename of YYYYMMDD.txt, returns a list of
    # ['YYYY', 'MM', 'DD']

    rawdate = os.path.splitext(os.path.basename(file))[0]

    date = [rawdate[0:4], rawdate[4:6], rawdate[6:]]

    return date

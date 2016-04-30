#!/usr/bin/python

import os

WWW = os.path.join("..","www")
CONFIG = os.path.join("config")

HEADER = []
FOOTER = []

infile = open(os.path.join(CONFIG, "header.txt"), 'r')
for line in infile:
    HEADER.append(line.rstrip())
infile.close()

infile = open(os.path.join(CONFIG, "header.txt"), 'r')
for line in infile:
    FOOTER.append(line.rstrip())
infile.close()

def write(outurl):
    outfile = open(os.path.join(WWW, outurl), "w")

    for line in HEADER:
        outfile.write(line)

    for line in write_placeholder():
        outfile.write(line)

    for line in FOOTER:
        outfile.write(line)

    outfile.close()

def write_placeholder():

    entry = [
        "<div id=\"tlogs\">",
        "<p><a name=\"$today\"></a><br /><br /></p>",
        "<div class=\"entry\">",
        "<h5><a href=\"$today\">DD</a> month YYYY</h5>",
        "<p>Feacby waeohaku aywoaeeo fepopo lyhili todepoae, taenga. Ypaogeni, ypnorani geahwaga diioanee aotrilco, aenoail. Oypo, weahipae kucogoyp fyeoim kyreeo? El godineng fengo aheoba himalidi trcoimao imypfe oaeha. In, trratr amlypoga cohitata macoipta? Ta, yeahta ahoyio, feanikre taneypel, bynekuim, enoyha. Adahilre, lylyno, aetaay aoimeo taquam toegeem? Rebyma maquag qunohi, fekyno fyniypdi. Eoaeby ikaeem goenkuao enacli, taliel agerhaza quema nonoimli. Ad amcory, aeypye raanaban lyaekuto coyega, adionige?</p>",
        "</div>"
    ]

    return entry

#!/bin/python2

import string
import sys
import json

# Yeah, I know. What else am I going to call it?
keys = {'[': '[', '{': '[', ']': ']', '}': ']', '\\': '\\', '|': '\\',
    ';': ';', ':' : ';', '\'': '\'', '\"': '\'', ',': ',', '<': ',', '.': '.',
    '>': '.', '/': '/', '?': '/', '-': '-', '_': '-', '=': '=', '+': '=',
    '`': '`', '~': '`'}

monograms = {}
digrams = {}

for char in list(string.ascii_lowercase):
    keys[char] = char
    keys[char.upper()] = char

for val in keys.values():
    monograms[val] = 0
    for val2 in keys.values():
        if val == val2:
            continue
        else:
        # the (key1, key2) pairs are sorted such that key1 < key2
            if val2 > val:
                digrams[(val, val2)] = 0
            elif val > val2:
                digrams[(val2, val)] = 0

# put the actual parsing code here

# ignore anything in "[" brackets "]"
# this means we can't actually record "[" or "]" presses, really.
# and probably shouldn't record "{" or "}" either, since those are the upper
# case on those keys
# "<-" is a backspace, ignore that string

if len(sys.argv) < 2:
    print "Missing argument: logfile."
    sys.exit(1)

log = open(sys.argv[1])

for line in log.readlines():
    # ignore the window annoucements
    # Only works if your keylog is from March or April
    if (line.startswith("[3/") or line.startswith("[4/")) and " pressed]" in line:
        continue
   
   # remove stuff like [ALT] or [Windows key]
    while "[" in line and "]" in line:
        line = line[:line.find("[")] + line[line.find("]")+1:]

    # remove backspaces, replacing them with spaces to avoid false positive
    # digrams from being counted
    line = line.replace("<-", " ")
    
    # empty lines are boring
    if line.isspace():
        continue
    
    # break into words
    words = line.split()
    for word in words:
        # iterate through letters
        for i in range(0, len(word)):
            if line[i] in keys:
                # update monogram frequency
                key1 = keys[line[i]]
                monograms[key1] += 1
                # if there's a following character, update digram frequency
                if i+1 < len(word) and line[i+1] in keys:
                    key2 = keys[line[i+1]]
                    if key1 < key2:
                        digrams[(key1, key2)] += 1
                    elif key2 < key1:
                        digrams[(key2, key1)] += 1


mono_out = open("monograms.data", "w")
di_out = open("digrams.data", "w")

mono_out.write(json.dumps(monograms))

json_dgram = {}
for (k1,k2), v in digrams.iteritems():
    json_dgram[k1+k2] = v

di_out.write(json.dumps(json_dgram))

mono_out.close()
di_out.close()
log.close()

# put the keyboard generation code here

nodes = {}

# simple graph class
class Graph:
    def __init__(self, key):
        self.weights = {}
        self.key = key
        self.freq = monograms[key]
        for (v1, v2), v3 in digrams.iteritems():
            if v1 == key or v2 == key:
                self.weights[v2] = v3
                self.weights[v1] = v3

'''
    def dagify(self):
        for edge in self.weights.keys():
            if self.key in nodes[edge].weights:
               del nodes[edge].weights[self.key]
'''
def graphcmp(x, y):
    if x.freq > y.freq:
        return 1
    elif x.freq < y.freq:
        return -1
    else:
        return 0

# create a node for each key
for key in keys.values():
   nodes[key] = Graph(key)

nodes_by_freq = sorted(nodes.values(), cmp=graphcmp, reverse=True)

for n in nodes_by_freq:
    print n.key, n.weights


# ASSUMPTIONS FOR KEYBOARD GOODNESS:
    # Alternating hands on common digrams is good
    # Home row > upper row > lower row
    # Prefer right hand over left hand
    # prefer index > middle > ring > pinky

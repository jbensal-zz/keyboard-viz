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
for key in keys.values():
    json_dgram[key] = {}
for (k1,k2), v in digrams.iteritems():
    json_dgram[k1][k2] = v
    json_dgram[k2][k1] = v

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

# we break the keyboard into sets in two ways:
# handedness of keypresses
left = [0] + range(3,8) + range(16, 21) + range(27,31)
right = [1,2] + range(8,16) + range(21,27) + range(31,37)
# and the row (or functional row, for 15 and 16)
top = [0,1,2,14,15]
upper = range(3,14)
home = range(16,27)
bottom = range(27,37)

dist_samehand = 4
dist_otherhand = 0
dist_samerow = 0
dist_1row = 1
dist_2row = 2
dist_3row = 3

scalar = 1

def distance(first, second, weight):
    mult = 1
    if (first in left and second in left) or (first in right and second in right):
        mult += dist_samehand
    else:
        mult += dist_otherhand
    if (first in upper and second in upper) or (first in home and second in home) or \
         (first in top and second in top) or (first in bottom and second in bottom):
        mult += dist_samerow
    elif (first in top and second in upper) or (second in upper and first in top) or \
        (first in home and second in upper) or (second in home and first in upper) or \
        (first in home and second in bottom) or (second in home and first in bottom):
        mult += dist_1row
    elif (first in top and second in home) or (first in home and second in top) or \
        (first in upper and second in bottom) or (first in bottom and second in home):
        mult += dist_2row
    else:
        mult += dist_3row
    
    return weight * mult * scalar
    
assignments = [None] * 37
priority = [22,23,24,19,18,17,21,20,25,16,26] # home row
priority += [8,9,7,10,6,11,12,5,4,13,3] # upper row
priority += [32,30,31,33,34,29,25,36,28,27] # bottom row
priority += [1,2,0] # top/terrible row
'''
n = nodes_by_freq.pop()
while len(priority) > 0:
    slot = priority.pop()
    assignments[slot] = n.key
    r
    mindist = None
    bestmatch = None 
    for key,weight in n.weights.iteritems():
        for p in priority:
            d = distance(slot, p, weight)
            if mindist = None or d < mindist:
                mindist = d
                bestmatch = key
'''

curr = nodes_by_freq.pop()
slot = priority.pop()
assignments[slot] = curr.key

w_scalar = 4
# while we still have to assign things
while len(priority) > 0:
    
    # determine the most importanct key to assign next
    importance_max = 0
    next_key = None
    for key,weight in curr.weights.iteritems():
        if key == curr.key or key in assignments:
            continue
        importance = weight * w_scalar + monograms[key]
        if importance > importance_max:
            importance_max = importance
            next_key = key

    # assign it to minimize distance
    min_dist = None
    new_slot = None
    for p in priority:
        d = distance(slot, p, curr.weights[next_key])
        if min_dist == None or d < min_dist:
            min_dist = d
            new_slot = p
    assignments[p] = next_key
    
    # set up for the next iteration
    del priority[priority.index(p)] # would del p work? probs not
    slot = p
    curr = nodes[next_key]

for x in keys.values():
    if x not in assignments:
        for slot in assignments:
            if slot == None:
                assignments[assignments.index(slot)] = x
                break

for x in keys.values():
    if x not in assignments:
        print x

layout = open("layout.data", "w")
layout.write(json.dumps(assignments))
layout.close()

'''
numtokey = {}
keytonum = {}
i = 0
for k in keys.values():
    if key in keytonum.keys():
        continue
    keytonum[key] = i
    i += 1

for key,num in keytonum.iteritems():
    numtokey[num] = key

def total_dist(guess):
    total = 0
    for n1 in guess:
        slot1 = guess.index(n1)
        for n2 in guess:
            slot2 = guess.index(n2)
            if slot2 >= slot1
                break
            weight = 0
            if n1 < n2:
                weight = digrams[(numtokey[n1],numtokey[n2])]
            else:
                weight = digrams[(numtokey[n2],numtokey[n1])]
            total += distance(slot1, slot2, weight)
    return total


qwerty = ['`', '-', '=', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'z', 'x', 'c', 'v',
            'b', 'n', 'm', ',' '.' '/']

'''
# ASSUMPTIONS FOR KEYBOARD GOODNESS:
    # Alternating hands on common digrams is good
    # Home row > upper row > lower row
    # Prefer right hand over left hand
    # prefer index > middle > ring > pinky

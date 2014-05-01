from PIL import Image
import json

keyb = Image.open("img/BLANK.png")
pix = keyb.load()
keys = json.loads(open("layout.data", 'r').read())
(width, height) = keyb.size
customlayout = {}
index = 0
positions = [[35, 120],
 [630, 120],
 [685, 120],
 [115, 174],
 [169, 174],
 [224, 174],
 [278, 174],
 [332, 174],
 [386, 174],
 [440, 174],
 [494, 174],
 [548, 174],
 [602, 174],
 [656, 174],
 [710, 174],
 [764, 174],
 [130, 225],
 [184, 225],
 [238, 225],
 [292, 225],
 [346, 225],
 [400, 225],
 [454, 225],
 [508, 225],
 [562, 225],
 [616, 225],
 [670, 225],
 [158, 275],
 [212, 275],
 [266, 275],
 [320, 275],
 [374, 275],
 [428, 275],
 [482, 275],
 [536, 275],
 [590, 275],
 [644, 275] ]
for y in range(height):
    for x in range(width):
        if pix[x, y] == (255, 0, 0, 255):
            key = keys[index]
            customlayout[str(key).upper()] = positions[index]
            if key == "\\":
                key = "bslash"
            elif key == "/":
                key = "fslash"
            elif key == ".":
                key = "dot"
            elif key == ";":
                key = "semi"
            keyb.paste(Image.open('img/'+key+'.png','r'), (x, y))
            index += 1

keyb.save("../img/CUSTOM.png")

keyboard_layouts = open("../keyboard-layouts.js", 'r')
firstline = keyboard_layouts.readline()
customline = keyboard_layouts.readline()
otherlayouts = keyboard_layouts.read()
keyboard_layouts = open("../keyboard-layouts.js", 'w')
keyboard_layouts.write(firstline)
keyboard_layouts.write("CUSTOM: "+json.dumps(customlayout)+",\n")
keyboard_layouts.write(otherlayouts)

from PIL import Image
import json

keyb = Image.open("img/BLANK.png")
pix = keyb.load()
keys = json.loads(open("layout.data", 'r').read())
(width, height) = keyb.size
index = 0
for y in range(height):
    for x in range(width):
        if pix[x, y] == (255, 0, 0, 255):
            key = keys[index]
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
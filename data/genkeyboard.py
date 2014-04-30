from PIL import Image

keyb = Image.open("img/BLANK.png")
pix = keyb.load()

img=Image.open('img/a.png','r')
(width, height) = keyb.size
for y in range(height):
    for x in range(width):
        if pix[x, y] == (255, 0, 0, 255):
            keyb.paste(img, (x, y))

keyb.save("img/custom.png")
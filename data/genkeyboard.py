from PIL import Image

keyb = Image.open("img/BLANK.png")
pix = keyb.load()
pix[0, 0] = (255, 0, 0, 255)

img=Image.open('img/a.png','r')
keyb.paste(img,(3,3))

keyb.save("img/custom.png")
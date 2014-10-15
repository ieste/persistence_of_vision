import Image
import ImageDraw
import ImageFont

fontname = "Arial"
fontsize = 11
text = "example@gmail.com"
colorText = "black"
colorOutline = "red"
colorBackground = "white"

img = Image.new('RGB', (200, 100), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 20), 'Hello', fill=(255, 0, 0))
text_width, text_height = d.textsize('Hello')


#font = ImageFont.truetype(fontname, fontsize)

width, height = text_width, text_height = d.textsize('Hello')
img = Image.new('RGB', (200, 100))
d = ImageDraw.Draw(img)
d.text((20, 20), text, fill=(255, 0, 0))

img.save("image.png")
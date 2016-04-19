from PIL import Image,ImageFont,ImageDraw
import numpy as np

font = ImageFont.truetype("msyh.ttf",32)

#convert word to utf-8 encoding, returned as a tuple
def w2u(u):
	assert(0x0800<=u<=0xffff)
	a = u%64+0x80
	u = u>>6
	b = u%64+0x80
	u = u>>6
	c = u%64+0xe0
	return c,b,a

def get_grey_scale(word):
	im = Image.new('L', (32, 32), 255)
	dr = ImageDraw.Draw(im)
	dr.text((0,-6), word, font=font)
	return np.array(im).mean()

def get_gs_dict():
	for u in range(0x4e00,0x9fb0):
		txt = bytearray(w2u(u)).decode()
		#todo: add
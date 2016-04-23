#!/usr/bin/env python3.5

from PIL import Image,ImageFont,ImageDraw
import numpy as np
import pandas as pd

font = ImageFont.truetype("wqy-zenhei.ttc",32)

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
	dict_list = []
	for u in range(0x20,0xff):
		try:
			txt = chr(u)
		except:
			print('error on decode %u'%u)
			continue
		grey = get_grey_scale(txt)
		dict_list.append((u, (grey, txt)))

		#progress bar
		if u%0x10==0:
			print('%f%%'%( (u-0x0000)/(0xff)*100 ))
	rslt = pd.DataFrame(dict(dict_list)).T
	return rslt

def nearest(n, li):
	diff = abs(n-li).min()
	if n+diff in li.values:
		return n+diff
	else:
		return n-diff

img = Image.open('test.jpg').convert('L')
img_arr = np.array(img.resize((250, 163)))

dct = get_gs_dict()
dct[0] -= dct[0].min()
m = dct[0].max()
r = 255/m
dct[0] *= r

li = dct[0]

a=''
idx=0
for arr in img_arr:
	a += ''.join([dct[dct[0]==nearest(x, li)][1].values[0] for x in arr])+'\n'
	print(idx)
	idx += 1
with open('img.txt', 'w') as f:
	f.write(a)

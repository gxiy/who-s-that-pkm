import os
from PIL import Image

"""
Generate silhouettes of all pokemon 1st gen using PIL
"""

def make_siloh(pkm_path):
#Use PIL to create silhouette of image
	im = Image.open(pkm_path)
	siloh = im.copy()
	width, height = siloh.size
	pix = siloh.load()

	for x in range(0, width):
		for y in range(0, height):
			r, g, b, a = pix[x,y]
			if a != 0:
				pix[x,y] = (0, 0, 0, 255)
	return siloh

def main(gen_name):
#Get pokemon image path list
	path = 'Images/Pokémon/' + gen_name
	spath = path + '/Silhouette/'
	pkm_paths = os.listdir(path)

	for pkm in pkm_paths:
		pkm_path = path + '/' + pkm
		pkm_siloh = make_siloh(pkm_path)
		pkm_spass = spath + 'siloh' + pkm
		pkm_siloh.save(pkm_spass)

main('1st Generation')




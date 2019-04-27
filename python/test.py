#!/usr/bin/env python
import sys
from coordinates import coordinates

min  = 100000000
info = ''
for cle,valeur in coordinates.items():

	for infos in valeur:

		if infos[0] == 'gene':

			infoCour = infos

			length = int(infos[5])-int(infos[4])
			print(length)

			if length < min:
				min = length
				info = str(infoCour)

				



print(min, info)

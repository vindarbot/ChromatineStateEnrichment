#!/usr/bin/env python

import os
import sys
from yattag import Doc
from name import name
from coordinates import coordinates
from state_to_gene import state_to_gene
from state_to_name import state_to_name
from results import results
from decimal import *

chiffre = 7.944690856271182e-23	

print(Decimal(chiffre).quantize(Decimal('.001'), rounding=ROUND_DOWN))


doc, tag, text = Doc().tagtext()

with tag('html'):

	with tag('head'):

		doc.stag('meta', charset="utf-8")

		doc.stag('link',rel='stylesheet', href='test.css')

		with tag('title'):

			text(name)

		




	with tag('body'):

		with tag('header'):

			with tag('h1'):

				text("Results")

		with tag('table'):

			with tag('thead'):

				with tag('tr'):

					header = ("State","Pvalue (input)","Oddsratio",
						"Nombre de gènes total (background)","Nombre de gènes totale ciblés  ",
						"Nombre de gènes input","Nombre de gènes input ciblés","Description","Sens","Pvalue (random sampling) ")

					for head in header:

						with tag('td',klass='head'):

							text(head)






			with tag('tbody'):

				for state, infos in sorted(results.items(), key=lambda kv: (kv[1][7],kv[1][0])):

					with tag('tr'):

						with tag('td'):

							text(state)




						for i in range(len(infos)):

								if infos[7] == 'over':

									with tag('td', klass='over'):

										text(infos[i])

								else:

									with tag('td', klass='under'):

										text(infos[i])







result = doc.getvalue()

with open('html/test.html', "w") as file:
    file.write(result)
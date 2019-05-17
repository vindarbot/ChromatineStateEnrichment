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




doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')

with tag('html'):

	with tag('head'):

		doc.stag('meta', charset="utf-8")

		doc.stag('link',rel='stylesheet', href='style.css')

		with tag('title'):

			text(name)

		doc.stag('link', rel='stylesheet', type='text/css', href='../javascript/DataTables/datatables.min.css')
		
		doc.stag('script', type='text/javascript', src ='../javascript/DataTables/datatables.min.js')

		with tag('script'):

			text(''' 
					$(document).ready( function () {
   						$('#example').DataTable();
						} );)''')
		




	with tag('body'):

		with tag('header'):

			with tag('h1'):

				text("Results")



		with tag("nav"):

			with tag("div"):


				with tag("ul"):

					with tag("li",):

						with tag("a", klass='nav', rel="external", href="index.html"):

							text("Main results")

						with tag("a", klass='nav', rel="external", href="genes.html"):

							text("Genes")

						with tag("a", klass='nav', rel="external", href="help.html"):

							text("Help")











		with tag('section', klass='table'):

			with tag('table', id='main_results'):

				with tag('thead'):

					with tag('tr'):

						header = ("State","Pvalue ajustée (input)","Oddsratio",
							"Nombre de gènes total (background)","Nombre de gènes totale ciblés  ",
							"Nombre de gènes input","Nombre de gènes input ciblés","Description","Sens","Pvalue ajustée (random sampling) ")

						for head in header:

							with tag('td',klass='head'):

								text(head)






				with tag('tbody'):



					for state, infos in sorted(results.items(), key=lambda kv: (kv[1][7],kv[1][0])):

						with tag('tr'):

							with tag('td'):

								with tag('a',klass='states', rel="external", href='states_'+str(state)+'.html'):

									text(state)




							for i in range(len(infos)):

									if infos[7] == 'over':

										with tag('td', klass='over'):

												text(infos[i])

									else:

										with tag('td', klass='under'):

											text(infos[i])

		doc.stag('img',src='../images/matrix.png',klass='matrix')






result = doc.getvalue()

with open('html/index.html', "w") as file:
    file.write(result)
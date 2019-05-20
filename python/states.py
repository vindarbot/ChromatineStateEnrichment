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
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--state",action='store')

args = parser.parse_args()

state = int(args.state)

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')

with tag('html'):

	with tag('head'):

		doc.stag('meta', charset="utf-8")

		doc.stag('link',rel='stylesheet', href='style.css')

		with tag('title'):

			text(name)

		doc.stag('link', rel='stylesheet', type='text/css', href='../javascript/DataTables/datatables.css')
		
		doc.asis("<script type='text/javascript' charset='utf-8' src ='../javascript/DataTables/datatables.js'></script>")

		with tag('script'):

			text(''' 
					$(document).ready( function () {
   						$('#table_states').DataTable();
						} );''')




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


		if results[state][7] == 'under':
			with tag("h3",style="color:#800000;"):
			

				text("state "+str(state)+" ( "+str(state_to_name[state])+")")
		else:
			with tag("h3",style="color:#006400;"):

				text("state "+str(state)+" ( "+str(state_to_name[state])+")")


		doc.stag('br')

		with tag("p", style="text-align: center;"):

			text("P-value : ")

			with tag('strong'):

				text(str(results[state][0]))



		with tag("div", klass='infos-background'):

			with tag("p"):

				text("Nombre de gènes total (background) : ")

				with tag('strong'):

					text(results[state][2])

			doc.stag('br')

			with tag("p"):

				text("Nombre de gènes total ciblés: ")

				with tag('strong'):

					text(results[state][3])


		with tag("div", klass='infos-input'):

			with tag("p"):

				text("Nombre de gènes input : ")

				with tag('strong'):

					text(results[state][4])

			doc.stag('br')

			with tag("p"):

				text("Nombre de gènes input ciblés: ")

				with tag('strong'):

					text(results[state][5])









		with tag('section', klass='table'):

			with tag("table", id="table_states"):

				with tag('tr'):

					header= ('Gene','ID','Description')

					for head in header:

						with tag('td',klass='head'):

							text(head)

				

				for gene in state_to_gene[state]:

					

					with tag('tr'):


						for i in range(len(gene)):

							if i == 0:

								with tag('td', klass='states'):

									with tag('a',real='external',href='genes.html#value='+gene[i], klass='links'): 
									# Permet de passer l'identifiant TAIR du gène cliqué dans l'URL, afin de le récupérer dansw la page gene.html,
									# Afin de placer le gène en question comme valeur par défault pour le formulaire.
										text(gene[i])

							else:

								with tag('td', klass='states'):

						

									text(gene[i])
					

		doc.asis("<script type='text/javascript' src='../javascript/states.js'></script>")

result = doc.getvalue()

with open('html/states_'+str(state)+'.html', "w") as file:
    file.write(result)




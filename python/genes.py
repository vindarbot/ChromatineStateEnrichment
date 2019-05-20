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






		with tag("div", klass='formulaire'):
			with tag("form", method='get'):

				with tag("label"):

					text("Enter a gene TAIR ID")

				doc.stag("input", type='text', placeholder='ex: AT1G01010', name='gene_input', id='gene_input')

				doc.stag("input", type='submit', value='Envoyer',name='submit_gene', id='submit_gene')


		with tag('canvas',id="canvas_gene",width="2400", height="1600"):

			text("Désolé, votre navigateur ne supporte pas Canvas. Mettez-vous à jour.")

		doc.asis("<script type='text/javascript' src='../javascript/coordinates.js'></script>")

		doc.asis("<script type='text/javascript' src='../javascript/results.js'></script>")
		
		doc.asis("<script type='text/javascript' src='../javascript/infos_states.js'></script>")

		doc.asis("<script type='text/javascript' src='../javascript/genes.js'></script>")




result = doc.getvalue()

with open('html/genes.html', "w") as file:
    file.write(result)
#!/usr/bin/env python

import scipy.stats as stats
from statsmodels.sandbox.stats.multicomp import multipletests
import sys
import os
import argparse
import re
import random
from argparse import RawTextHelpFormatter
from collections import defaultdict
from state_to_name import state_to_name
from  At_all_genes import At_all_genes

parser = argparse.ArgumentParser(description='test of overrepresentation of\
	chromatin state in a list of specific genes\n\n\
	Exemple: python3 fisher_chrState.py 3 DEG/Col_ColHS/id.txt',
	formatter_class=RawTextHelpFormatter)


parser.add_argument("--state",action='store_true',
	help="having state name from state number\n")

parser.add_argument("-l","--list", action='store', 
	help="list of genes to analyse overrepresentation of epigenetic mark")

parser.add_argument("-o","--output", action='store', 
	help="output directory for results files (default= current directory)",
	default="")

parser.add_argument("-p","--pvalue",action='store',
	help="p-value associate to the exact fisher test for overepresentation of chromatin state (default=0.01) ",
	default=0.01)

args = parser.parse_args()

if args.state:
	print("\nlist of chromatin states possible:\n\
state	Preferential Epigenetics Marks		Preferential location\n\
1		H3.3						3'UTR\n\
2		H3.3 histone acetylation,H3K4me2,H2A.Z		CDS,3'UTR\n\
3		H3K4me1,H3.3,H3.1				CDS\n\
4		H3K4me1,H3.3					CDS,intron\n\
5		H3K4me1,H3K36me3,H3.3,H3.1			CDS\n\
6		H3K4me1,H3K36me3				intron\n\
7		H3K4me1,H3K36me3,H3K4me2			CDS,intron\n\
8		H3K4me1,H3K4me2,H2A.Z				CDS\n\
9		H3K4me1						intron\n\
10		H2A.Z						CDS,intron\n\
11		H3K27me3,H2A.Z,H3K4me2				CDS\n\
12		H3K27me3,H2A.Z					Promoter,CDS,intron,intergenic\n\
13		H3K27me3,H2A.Z					Promoter,intergenic\n\
14		H3K27me3					Promoter,intergenic\n\
15		H3K27me3,accessible DNA				Promoter,intergenic\n\
16		accessible DNA					Promoter,intergenic\n\
17		accessible DNA					Promoter\n\
18		accessible DNA					Promoter\n\
19		accessible DNA					Promoter,snRNA\n\
20		accessible DNA 					Promoter\n\
21		accessible DNA					Promoter\n\
22		histone acetylation,H3K4me2			coding gene,miRNA,snoRNA\n\
23		accessible DNA,H3K36ac,H3K56ac,H4K16ac,H3K4me3	Promoter,5'UTR\n\
24		accessible DNA,histone acetylation,H3K4me3	5'UTR,snoRNA\n\
25		histone acetylation,H3K4me3,H3K4me2,H2A.Z	intron\n\
26		histone acetylation,H3K4me3,H3K4me2,H2A.Z	CDS\n\
27		H3K4me2,histone acetylation,H3K4me3,H2A.Z	CDS\n\
28		H3K4me3,H3K4me2,H2A.Z				intron\n\
29		weak signal					intergenic\n\
30		rare signal					intergenic\n\
31		DNA methylation,H3K9me2,H3K27me3		intergenic,miRNA\n\
32		DNA methylation,H3K9me2				intergenic,TE\n\
33		H3K9me2,DNA methylation				TE\n\
34		H3K9me2,DNA methylation,H3K27me1		TE,miRNA\n\
35		H3K9me2,DNA methylation,H2A.X			intergenic,pericentromere\n\
36		CENH3,H3K9me2,DNA methylation,accessible DNA	rRNA,tRNA,centromere\n\n")
	exit(0)

### Variables





### Definitions

def rounding(chiffre):

	if re.search("e",str(chiffre)):

		start = re.compile("[0-9][.][0-9]{2}")
		end = re.compile("e-[0-9]+")

		return float("".join(start.findall(str(chiffre))+end.findall(str(chiffre))))

	elif re.search("[0][.][0]{2}",str(chiffre)):

		motif = re.compile("[0][.][0]+[0-9]{2}")

		return float("".join(motif.findall(str(chiffre))))

	else:

		return chiffre


def retrieve_input_genes(liste):
	''' Récupérer les gènes ID TAIR à partir du fichier fournit par l'utilisateur'''

	with open(liste,'r') as fp:

		# Récupérer le nom du fichier
		name = os.path.basename(os.path.splitext(liste)[0])

		list_read = fp.read()
		# Expression régulière pour définir les id TAIR
		regex_TAIRID = re.compile("AT[A-Z0-9]{1}G[0-9]{5}")
		# Récupérer le nom du fichier, ainsi que l'ensemble des ids au sein du fichier 
		# fournit par l'utilisateur
		return name, regex_TAIRID.findall(list_read)





def counting_target_per_state(genes,states):
	''' Pour chacun des 36 chromatines states, compter le nombre de gène totale ciblé par le state (target_background),
	ainsi que le nombre de gènes ciblé par le state dans la liste donnée par l"utilisateur (target_input)'''

	# Initialisation de deux dicos, un pour récupérer le nombre des gènes ciblés par chaque chromatine state
	# au sein de la liste founrit par l'utilisateur (input) ainsi que le nombre total de gènes ciblés 
	# par le chromatine state (background)
	target_input = dict((i,[]) for i in states )

	target_background = dict((i,0) for i in states )

	# Fichier At_genes_states.txt, 1ère colonne le numéro du chromartine state, 2ème colonne id des gènes ciblés
	# par le chromatine state.
	with open("data/At_genes_states.txt","r") as file:

		for ligne in file.readlines():

			ligne = ligne.split("\t")
			# Après avoir séparer chaque ligne par les tabulation (".split("\t")), la premier élément de la liste (ligne[0])	
			# permet d'accéder au numéro du chromatine state.
			if int(ligne[0]) in states:
				# A chaque ligne, on incrémente le nombre de cibles background de 1 quand on tombe sur le state en question
				target_background[int(ligne[0])] += 1
				# ligne[1] renvoit au gène, si le gène est présent dans la liste fournit par l'utilisateur, on incrémente le nombre
				# de cibles input pour le state en question de 1
				if ligne[1] in genes:

					target_input[int(ligne[0])].append([ligne[1],ligne[2],ligne[4]])

	return target_background, target_input



def bonferroni_correction(pvalues, seuil):

	p_adjusted = multipletests(pvalues, method='bonferroni', alpha=0.01)

	return list(list(p_adjusted)[1])


def running_stat_part(target_background, genes_input, target_input):
	''' Test de fisher exact entre le rapport du nombre total de gènes chez Arabidopsis
	sur le nombre de gènes ciblés par le state (effrectif attendu) et le nombre de total
	de gènes donné en entrée sur le nombre de gènes en entrée ciblé par le state '''

	# Nombre de gènes total au sein du génome de référence d'Arabidopsis Thaliana. (TAIR10)
	len_genes_background = 33602
	# Pour récupérer les résultats du test de fisher.
	state_results = {}
	# Pour les states en question (utile pour le random samplempling quand on s'intéresse qu'à la liste
	# des states significatifs.)
	to_adj = []

	for state in list(target_background.keys()):


			# On récupère le ratio rapport attendu/rapport de la liste fournit, ainsi que la p-value
			# associé au test de fisher

		oddsratio, pvalue = stats.fisher_exact([[len_genes_background,
				target_background[state]], [len(genes_input), len(target_input[state])]])

		pvalue = rounding(pvalue)
		to_adj.append(pvalue)

		oddsratio = round(oddsratio,2)

		state_results[state] = [pvalue,oddsratio,len_genes_background,
			target_background[state],len(genes_input),
			len(target_input[state]),state_to_name[state]]

	padj = bonferroni_correction(to_adj,args.pvalue)

	count = 0

	for state in list(target_background.keys()):

		state_results[state][0] = rounding(padj[count])
		count += 1

	return state_results



def retrieve_significative_states(results,target_input):
	''' Retenir uniquement les states dont le fisher test donne une p-value inférieur
	à celle donnée en paramètre '''

	# Pour l'ensemble des states
	for state in range(1,37):
		# On récupère la p-value et le ratio
		padj = results[state][0]
		oddsratio = results[state][1]
		# Si la p-value est significative (cf p-value fournit par l'utilisateur, défault = 0.01)
		# Et le rapport inférieur à 1 (RNombre de gènes de la liste ciblé inférieur à celui attendu) )
		if padj < args.pvalue and oddsratio < 1:

			results[state].append("under")
		# Sinon si la p-value est sign et le rapport supérieur à 1
		elif padj < args.pvalue and  oddsratio > 1:

			results[state].append("over")
		# Sinon, si la p-value de la chromatine state n'est pas signifciative, on supprime la state des
		# résultats
		else:

			del results[state]
			del target_input[state]


	return results


def counting_state_per_gene(target_input, signif_states):
	''' Pour chaque gène, retourné l'ensemble des states significatives qui ciblent
	le gène '''

	gene_to_state = defaultdict(list)

	for state, genes in target_input.items():

		for infos in genes:

			gene_to_state[infos[0]].append(state)

	return gene_to_state



def retrieve_coordinates(gene_to_states, signif_states):
	''' Récupérer les coordonnées du gène impliqué, ainsi que de tous les signaux 
	des states significatives visant le gène '''

	coordinates_genes = defaultdict(list)
	# Le fichier At_segments_states.txt comprend tous les signaux associés à chaque chromatine state.
	file1 = open("data/At_segments_states.txt")

	lignes = file1.readlines()
	# On formate la 4ème colonne (ligne.split()[3]) pour enlever le "E" devant le nuémro du chromatine state
	# Ainsi, on ne conserve que les lignes associés aux chromatines states qui sont significatives ("in signif_states")
	lignes = [ligne for ligne in lignes if int(ligne.split()[3].lstrip("E")) in signif_states]


	with open("data/At_genes_states.txt","r") as file:

		for ligne in file.readlines():

			ligne = ligne.split("\t")
			# On récupère ici les coordonnées des gènes ciblés par au moins une chromatine state significative
			if ligne[1] in gene_to_states.keys() and ligne[1] not in coordinates_genes.keys():

				coordinates_genes[ligne[1]].append(["gene",ligne[2],ligne[4],ligne[5],ligne[6],ligne[7],ligne[8]])



	for gene in coordinates_genes.keys():

#		Chr = coordinates_genes[gene][0][1]
#		start = int(coordinates_genes[gene][0][4])
#		end = int(coordinates_genes[gene][0][5])

		for ligne in lignes:

			ligne = ligne.split()

			# Pour chaque gène, on récupère les signaux des chromatines states qui ciblent le gène (fourchette -1000 nt en downstream, +1000 nt en upstream)

			if int(ligne[3].lstrip("E")) in signif_states and ligne[0] == coordinates_genes[gene][0][3] and ( int(ligne[2]) in range(int(coordinates_genes[gene][0][4])-1000,int(coordinates_genes[gene][0][5])+1000) or 
				int(ligne[1]) in range(int(coordinates_genes[gene][0][4])-1000,int(coordinates_genes[gene][0][5])+1000) ):

				coordinates_genes[gene].append([int(ligne[3].lstrip("E")), ligne[0], ligne[1], ligne[2]])

	return coordinates_genes







def random_sampling(genes, nb_genes, states, results, n):
	''' Échantillonage aléatoire du même nombre de gènes que la liste de gène
	fournit par l'utilisateur (parmis l'ensemble des gènes d'Arabido), 
	et test de fisher sur cet échantillon pour voir si les states significatives 
	ne sont pas du au hasard '''

	pvalues = defaultdict(int)

	for i in range(int(n)):

		print("Random Sampling "+str(i+1)+"/"+str(n))

		sample = random.sample(genes,nb_genes)

		background, input = counting_target_per_state(sample,states)

		random_results = running_stat_part(background, sample, input)

		for state in random_results.keys():

			pvalues[state] += random_results[state][0]

	for state in pvalues.keys():

		pvalues[state] = pvalues[state]/int(n)

		results[state].append(pvalues[state])


	return results


def write_output(name, outdir, signifs, gene_states, coordinates, target_input):
	'''Écriture du fichier de résultat'''

	if outdir is not "":

		outdir = outdir+"/"

		if not os.path.isdir(outdir):

			os.mkdir(outdir)

	with open(outdir+"results_states.txt","w") as file:

		file.write("state\tp_value\toddsratio\trandom_sampling\tnb_genes_background\t\
			nb_target_state\tnb_genes_input\tnb_target_input\tsens\n")

		for b in sorted(signifs.items(), key=lambda kv: (kv[1][7],kv[1][0])):

			file.write(str(b[0])+"\t"+str(b[1][0])+"\t"+str(b[1][1])+"\t"+
				str(b[1][8])+"\t"+str(b[1][2])+"\t"+str(b[1][3])+"\t"+str(b[1][4])+
				"\t"+str(b[1][5])+"\t"+str(b[1][6])+"\t"+str(b[1][7])+"\n")


	with open(outdir+"genes_to_states.txt","w") as file:

		file.write("gene\tstates\n")

		for gene, states in gene_states.items():

			file.write(gene+"\t")

			for state in states:

				file.write(str(state)+" ")

			file.write("\n")


	with open(outdir+"coordinates_signals.txt","w") as file:

		coordinates = dict(coordinates)

		for gene, coordinate in coordinates.items():

			for i in range(len(coordinate)):

				if i == 0 : 

					file.write(str(gene)+"\t"+str(coordinate[i][3])+"\t"+str(coordinate[i][4])+"\t"+str(coordinate[i][5])+"\n")

				else:

					file.write(" \t"+str(coordinate[i][0])+"\t"+str(coordinate[i][2])+"\t"+str(coordinate[i][3])+"\n")


	with open(outdir+"state_to_genes.txt","w") as file:

		for state,genes in target_input.items():

			file.write(str(state)+"\t")

			for gene in genes:

				for info in gene:

					file.write(info+"\t")

			file.write("\n")




	with open("python/name.py","w") as file:

		file.write("name = '"+name+"'")

	with open("javascript/coordinates.js","w") as file:

		file.write("coordinates = "+str(coordinates))

	with open("python/state_to_gene.py","w") as file:

		file.write("state_to_gene = "+str(target_input))

	with open("python/results.py","w") as file:

		file.write("results = "+str(signifs))

	with open("javascript/results.js","w") as file:

		file.write("results = "+str(signifs))

	with open('python/gene_to_states.py','w') as file:

		file.write('gene_to_states ='+str(dict(gene_states)))




if os.path.isfile(args.list):

	name, genes_input = retrieve_input_genes(args.list)

else:
	print("Please give a correct list of genes file")
	exit(0)
	

print("Counting number of genes per state")
background, input = counting_target_per_state(genes_input, range(1,37))

print("Running fisher test for every state")
results = running_stat_part(background, genes_input,input)

print("Retrieving significatives states")
states_signif = retrieve_significative_states(results,input)

print("Running Random Sampling")
final_results = random_sampling(At_all_genes, len(genes_input),
list(states_signif.keys()), states_signif , 1)

print("Counting number of significatives states per gene")
gene_to_states = counting_state_per_gene(input,list(states_signif.keys()))

print("Retrieving coordinates of signals per gene")
coordinates = retrieve_coordinates(gene_to_states,list(states_signif.keys()))



# random_sampling(At_all_genes, len(genes_input), list(states_signif.keys()))

write_output(name, args.output, final_results, gene_to_states, coordinates, input)




os.system("python3 python/matrix.py")

os.system("Rscript R/matrix_states.R")

os.system("python3 python/index.py")



from state_to_gene import state_to_gene

for state in state_to_gene.keys():

	os.system("python3 python/states.py --state "+str(state)+"")

os.system("python3 python/genes.py")




















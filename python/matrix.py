import sys
import re
import re
from gene_to_states import gene_to_states
from state_to_gene import state_to_gene
from state_to_name import state_to_name

dirname = os.path.dirname
CSE_PATH = dirname(dirname(os.path.realpath(__file__)))

with open(CSE_PATH+'/R/matrix.txt','w') as file:

	states_sign = []

	file.write('\t')

	for i in range(1,37):

		if i in state_to_gene:

			file.write(state_to_name[i]+'\t')

			states_sign.append(i)

	file.write('\n')

	for gene, states in gene_to_states.items():

		file.write(gene)

		file.write('\t')

		for i in states_sign:

			if i in states:

				file.write('1\t')

			else:

				file.write('0\t')

		file.write('\n')










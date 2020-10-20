# ChromatineStateEnrichment (CSE)

With a list of Arabidopsis thaliana genes as input (TAIR ID format), the tool CSE performs an enrichment analysis to see if these genes are preferentially targeted by some epigenetics marks.

The 36 epigenetics marks and the genes associated were described by Liu Y., et al. (PCSD: a plant chromatin state database. Nucleic Acids Research, Volume 46, Issue D1, 4 January 2018, Pages D1157–D1167, https://doi.org/10.1093/nar/gkx919)

The first step of CSE performs statistical tests (Fisher's exact test). The second part allows the user to visualize the location of the enriched marks inside the genes given as input.

The tool is a part of RNA-Seq pipeline (https://github.com/Darbinator/RNA_Seq_Pipeline) which also allows to identify differently expressed genes (DEG), and differentially alternatively spliced genes (DSAG), from RNA_Seq data. CSE is in this case execute with the list of DEG.

## Initialisation

Download the tool

> git clone https://github.com/Darbinator/ChromatineStateEnrichment.git

Download associated packages

> pip3 install statsmodels

> pip3 install yattag

## Utilisation

List of genes as input must be a list of A. thaliana genes in the TAIR ID format, with one gene par line :

AT1G01010

AT1G01020

AT1G01030

...

To run the analysis:

> python3 python/fisher_chrState.py -l list_of_genes.txt -o output.txt 

To see the description of all epigenetics marks, please use:

> python3 python/fisher_chrState.py --state

## Output

### html/index.html

> open html/index.html

Open a html page to visualise the results 

### results_states.txt:

Global results of the enrichment analysis.

### genes_to_states.txt 

Input genes (first column) and enriched marks associated (Second column)

### state_to_genes.txt

Each column represent an enriched mark, with genes accosiated


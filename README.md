# ChromatineStateEnrichment (CSE)

From a list of Arabidopsis thaliana genes (TAIR ID format), the tool CSE performs an enrichment analysis to see if these genes are preferentially targeted by some epigenetics marks.

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
AT1G01040
AT1G01046
...

To run the analysis:

> python3 python/fisher_chrState.py -l list_of_genes.txt -o output.txt 

## Output

### html/index.html

> open html/index.html

Open a html page to visualise the results 

### results_states.txt:

Global results of the enrichment analysis. Exemple:

state	p_value	oddsratio	random_sampling	nb_genes_background		nb_target_state	nb_genes_input	nb_target_input	sens
20	0.00094	2.15	1.0	33602	8129	98	51	accessible DNA over
18	0.001	2.06	0.20875248332485308	33602	9677	98	58	accessible DNA 	over
32	0.0013	0.0	1.0	33602	3911	98	0	DNA methylation,H3K9me2 (TE)	under
33	0.0014	0.0	1.0	33602	3968	98	0	H3K9me2,DNA methylation (TE)	under

### genes_to_states.txt 

Input genes (first column) and enriched marks associated (Second column)

### state_to_genes.txt

Each column represent an enriched mark, with genes accosiated

## Infos

Number of the chromatin state (firt column) and description of the mark: (You can retrieve this table with --state tag)

state	Preferential Epigenetics Marks		Preferential location
1		H3.3						3'UTR
2		H3.3 histone acetylation,H3K4me2,H2A.Z		CDS,3'UTR
3		H3K4me1,H3.3,H3.1				CDS
4		H3K4me1,H3.3					CDS,intron
5		H3K4me1,H3K36me3,H3.3,H3.1			CDS
6		H3K4me1,H3K36me3				intron
7		H3K4me1,H3K36me3,H3K4me2			CDS,intron
8		H3K4me1,H3K4me2,H2A.Z				CDS
9		H3K4me1						intron
10		H2A.Z						CDS,intron
11		H3K27me3,H2A.Z,H3K4me2				CDS
12		H3K27me3,H2A.Z					Promoter,CDS,intron,intergenic
13		H3K27me3,H2A.Z					Promoter,intergenic
14		H3K27me3					Promoter,intergenic
15		H3K27me3,accessible DNA				Promoter,intergenic
16		accessible DNA					Promoter,intergenic
17		accessible DNA					Promoter
18		accessible DNA					Promoter
19		accessible DNA					Promoter,snRNA
20		accessible DNA 					Promoter
21		accessible DNA					Promoter
22		histone acetylation,H3K4me2			coding gene,miRNA,snoRNA
23		accessible DNA,H3K36ac,H3K56ac,H4K16ac,H3K4me3	Promoter,5'UTR
24		accessible DNA,histone acetylation,H3K4me3	5'UTR,snoRNA
25		histone acetylation,H3K4me3,H3K4me2,H2A.Z	intron
26		histone acetylation,H3K4me3,H3K4me2,H2A.Z	CDS
27		H3K4me2,histone acetylation,H3K4me3,H2A.Z	CDS
28		H3K4me3,H3K4me2,H2A.Z				intron
29		weak signal					intergenic
30		rare signal					intergenic
31		DNA methylation,H3K9me2,H3K27me3		intergenic,miRNA
32		DNA methylation,H3K9me2				intergenic,TE
33		H3K9me2,DNA methylation				TE
34		H3K9me2,DNA methylation,H3K27me1		TE,miRNA
35		H3K9me2,DNA methylation,H2A.X			intergenic,pericentromere
36		CENH3,H3K9me2,DNA methylation,accessible DNA	rRNA,tRNA,centromere


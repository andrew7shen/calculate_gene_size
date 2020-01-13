#Andrew Shen
import re
import sys
from operator import itemgetter

###Purpose: Calculates the exon size of the genes.

###To run this program, go to the command line and specify four parameters:
###python addCodingSize_exons.py (input file) (output file)

###This set of four lines takes an input file from the command line, and sets the contents of the file to a variable "contents".
input_file = sys.argv[1]
read = open(input_file, "r")
contents_input = read.read()

###This piece of code divides the input file by a newline delimiter.
data_newline = contents_input.splitlines()
###There are 5121 gene inputs.

###This piece of code divides the input file by a tab delimiter.
data_tab = []
for item in data_newline:
	data_tab.append(item.split("\t"))

###This piece of code keeps only the name of the gene and the start and end exons.
data_final = []
for item in data_tab:
	data_final.append(itemgetter(9,10,12)(item))
del data_final[0]

###This piece of code creates a list of gene names.
gene_names = [] ###To initialize the variable.
for item in data_final:
	gene_names.append(item[2])

###Creates a list in which each item is a list of startExons and endExons for each gene.
values = []
for item in data_final: #alternating tuples of exon starts and ends
	values.append(item[0].split(","))
	values.append(item[1].split(","))
values_int = []
for item in values:
	del item[len(item) - 1] #because empty item after each list
	values_int.append(map(int, item)) #converts every string item an int
values_ordered = [values_int[x:x+2] for x in range(0, len(values_int),2)] #condensed for loop, creates list with each item being the start and end exons of a gene
del values_ordered[len(values_ordered)-1]

###Sets total coding size of each gene to sizes.
sizes = []
for item in values_ordered:
	sizes.append(sum([(y - x)-1 for (x,y) in zip(item[0], item[1])])) #accesses same index of two containers

###Creates a dictionary gene_dict that with the gene name as the key and the different coding size as the value.
gene_dict = {}
for k,v in zip(gene_names,sizes):
	if k not in gene_dict:
		gene_dict[k] = [v]
	else:
		gene_dict[k].append(v) ###If there is already a coding size for a gene, appends the new coding size to the value.

###Keeps only the largest coding size.
new = {}
for gene in gene_dict:
	if len(gene_dict[gene]) == 1:
		new[gene] = gene_dict[gene][0]
	else:
		greatest = 0
		for item in gene_dict[gene]:
			if item > greatest:
				greatest = item
		new[gene] = greatest

###This piece of code formats the data into a text file with two columns: one for the gene name and one for the gene size.
final_printed = ""
for gene in new:
	final_printed += gene + "\t" + str(new[gene]) + "\n"

###This piece of code writes pairs of gene names and gene sizes to the output file.
output_file = sys.argv[2]
write = open(output_file, "w")
write.write(str(final_printed))
write.close()
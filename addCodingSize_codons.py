#Andrew Shen
import re
import sys
from operator import itemgetter

###To run this program, go to the command line and specify four parameters:
###python addCodingSize_codons.py (input file) (output file)

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

###This piece of code keeps only the name of the gene and the start and end codons.
data_final = []
for item in data_tab:
	data_final.append(itemgetter(6,7,12)(item))
del data_final[0]

###This piece of code calculates the gene size by subtracting the start of the codon from the end of the codon.
size_and_name = []
for item in data_final:
	size_and_name.append(itemgetter(2)(item))
	size_and_name.append(int(item[0]))
	size_and_name.append(int(item[1]))
	size_and_name.append((int(item[1])-int(item[0]))+1)

###This piece of code creates a list of gene names and a list of gene sizes.
gene_names = 0 ###To initialize the variable.
gene_names = size_and_name[::4]

###This piece of code takes the list size_and_name and splits it up by every four items.
gene_list = [size_and_name[x:x+4] for x in range(0, len(size_and_name),4)]
del gene_list[len(gene_list)-1]
###We now have a list containing 5121 gene names with their startCodons, endCodons, and gene sizes.

###This piece of code takes the list of gene names and gene sizes, and sets it to a a dictionary; the key is the 
###gene name and the value is a list of lists: each list within the list describes [startCodon, endCodon, gene size].
old = {}
for item in gene_list:
	if item[0] not in old:
		old[item[0]] = [[item[1], item[2], item[3]]]
	else:
		old[item[0]].append([item[1], item[2], item[3]])

print(old)

###This piece of code adds up all the different positions and ranges of each gene.
new = {}
for gene in old:
	if len(old[gene]) == 1:
		new[gene] = old[gene][0]
	else:
		new[gene] = old[gene][1]
		for rangeList in old[gene]:
			if rangeList[0] >= new[gene][0] and rangeList[0] < new[gene][1] and rangeList[1] > new[gene][0] and rangeList[1] <= new[gene][1]:
				#if start and end of tested item's range within current item's range, ignored
				break
			elif rangeList[0] >= new[gene][0] and rangeList[0] < new[gene][1] and rangeList[1] > new[gene][1]:
				#if start within tested item's range but end is farther than current item's end, new range calculated
				new[gene] = [rangeList[0], new[gene][1], (new[gene][1] - rangeList[0]) + 1]
				break
			elif rangeList[0] < new[gene][0] and rangeList[1] > new[gene][0] and rangeList[1] <= new[gene][1]:
				#if start of tested item's range before current range and end is within current range, new range calculated
				new[gene] = [rangeList[0], new[gene][1], (new[gene][1] - rangeList[0]) + 1]
				break
			elif rangeList[0] < new[gene][0] and rangeList[1] > new[gene][1]:
				#if start and end of tested item's range outside current range, new range calculated
				new[gene] = [rangeList[0], rangeList[1], (rangeList[1] - rangeList[0]) + 1]
				break
			else:
				break

###This piece of code takes the dicionary of the final start, end, and gene size for each gene, and keeps only the gene size.
final = {}
for gene in new:
	final[gene] = new[gene][2]

###This piece of code formats the data into a text file with two columns: one for the gene name and one for the gene size.
final_printed = ""
for gene in final:
	final_printed += gene + "\t" + str(final[gene]) + "\n"

###This piece of code writes pairs of gene names and gene sizes to the output file.
output_file = sys.argv[2]
write = open(output_file, "w")
write.write(str(final_printed))
write.close()
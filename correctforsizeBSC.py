#Andrew Shen
import sys
import re

###To run this program, go to the command line and specify four parameters:
###python correctforsizeBSC.py (input file 1) (input file 2) (output file)
###For this program, (input file 1) is the output file for the program addCodingSize_exons (output_exons.txt) and
###(input file 2) is the file BSCdata.txt (contains data about number of mutations per gene)

###Sets the two input files to different variables: "codingsize" and "BSCdata"
input_file = sys.argv[1]
read = open(input_file, "r")
codingsize = read.read()

input_file = sys.argv[2]
read = open(input_file, "r")
BSCdata = read.read()

###Cleans up the BSC data into a dictionary (mutations) with (key = gene) and (value = total number of mutations per gene)
BSCdata_newline = BSCdata.splitlines()
BSCdata_tab = []
for item in BSCdata_newline:
	BSCdata_tab.append(item.split("\t"))
del BSCdata_tab[0]

mutation_count = {}
for item in BSCdata_tab:
	del item[1]
	item[:] = [x for x in item if x != "."] #keeps only items that aren't periods
	mutation_count[item[0]] = [] #creates new dictionary item with gene name as key and empty list as value
	for value in item[1:]:
		mutation_count[item[0]].append(int(value[0])) #adds all mutation counts to the dictionary
for key in mutation_count:
	mutation_count[key] = sum(mutation_count[key])###1113 genes

###Calculates the number of mutations per gene / gene size using the output_exons data file and the mutation_count dictionary
codingsize_newline = codingsize.splitlines()
codingsize_tab = []
for item in codingsize_newline:
	codingsize_tab.append(item.split("\t"))

codingsize_dict = {}
for item in codingsize_tab:
	item[1] = float(item[1]) / 1000#Converts to kilobase pairs
	codingsize_dict[item[0]] = item[1]#1615 genes

corrected = {}
for key in codingsize_dict:
	if key in mutation_count:
		corrected[key] = round((mutation_count[key] / codingsize_dict[key]), 3) #round to three decimal places

###Formats the data into a text file with two columns: one for the gene name and one for the mutation rate (mutations per gene / gene size).
final_printed = ""
for key in corrected:
	final_printed += key + "\t" + str(corrected[key]) + "\n"

###This piece of code writes pairs of gene names and mutation rates to the output file.
output_file = sys.argv[3]
write = open(output_file, "w")
write.write(str(final_printed))
write.close()
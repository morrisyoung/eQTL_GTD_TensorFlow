import numpy as np






if __name__ == "__main__":






	##============================================================================================================
	## get gene list from read count file
	##============================================================================================================
	filename = "./data_raw/gencode.v19.genes.v6p_model.patched_contigs.gtf"
	file = open(filename, 'r')
	file.readline()
	file.readline()
	file.readline()
	file.readline()
	file.readline()
	file.readline()		## extra line for this version

	repo_gene = {}
	repo_gene_name = {}
	while 1:
		line = (file.readline()).strip()
		if not line:
			break

		##
		line = line.split()
		chr = line[0]
		tss = line[3]
		gene = line[9][1: -2]
		gene_name = line[17][1:-2]

		#print line
		#break



		##
		type = line[2]
		if type == "gene":
			repo_gene[gene] = 1
			repo_gene_name[gene_name] = 1
	file.close()



	print len(repo_gene)
	print len(repo_gene_name)









	##
	'''
	filename = "./data_raw/GTEx_Analysis_v6p_RNA-seq_RNA-SeQCv1.1.8_gene_reads.gct"
	file = open(filename, 'r')
	file.readline()
	file.readline()
	file.readline()

	count = 0
	while 1:
		line = (file.readline()).strip()
		if not line:
			break

		line = line.split()
		gene = line[0]

		if gene in repo_gene:
			count += 1
	file.close()
	print count
	'''
	######## --> why all the genes from read count file are annotated as "gene"?










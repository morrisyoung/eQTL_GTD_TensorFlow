## this is the tensor init series, which involves three parts (three scripts):
##	1. PCA on (sample x gene) matrix, to get gene factor matrix and the smaller tensor of (indiv x tissue x factor)
##	2. do the incomplete PCA with R, and get individual factor matrix and tissue factor matrix
##	3. re-solve the linear system with LASSO of (sample x gene) and (sample x factor) [from indiv and tissue fm] to get sparse gene fm


## this script takes the preprocessed and normalized tensor as input
## this script will get accompany with incomplete PCA R script (for indiv and tissue fm), and LASSO script (for gene fm)
## this script will be followed by Beta init


## output:
##	T, U, V






##===============
##==== libraries
##===============
import numpy as np
from numpy.linalg import inv
from scipy.stats import wishart
import math
from numpy import linalg as LA
from copy import *
import cProfile
import timeit
from sklearn.decomposition import PCA
import re





K = 28
I = 0
J = 0
D = 400





if __name__ == "__main__":





	##=============
	##==== loading
	##=============
	##==== I
	repo_indiv = {}
	for k in range(K):
		list_pos = np.load("../preprocess/data_train/Tensor_tissue_" + str(k) + "_pos.npy")
		for pos in list_pos:
			repo_indiv[pos] = 1
	I = len(repo_indiv)
	print "there are # of individuals:", I


	##==== J
	data = np.load("../preprocess/data_train/Tensor_tissue_0.npy")
	J = len(data[0])
	print "there are # of genes:", J


	##==== Data, Data_index
	Data = []							## matrix of sample x gene
	Data_index = []						## matrix of sample x pos (tissue, indiv)
	for k in range(K):
		data = np.load("../preprocess/data_train/Tensor_tissue_" + str(k) + ".npy")
		list_pos = np.load("../preprocess/data_train/Tensor_tissue_" + str(k) + "_pos.npy")

		for i in range(len(data)):
			exp = data[i]
			pos = list_pos[i]

			Data.append(exp)
			Data_index.append((k, pos))
	Data = np.array(Data)
	Data_index = np.array(Data_index)


	print Data.shape
	print Data_index.shape






	##=============
	##==== do PCA for Sample x Gene matrix
	##=============
	print "performing PCA..."
	n_factor = D
	pca = PCA(n_components=n_factor)
	pca.fit(Data)
	Y2 = (pca.components_).T
	Y1 = pca.transform(Data)
	variance = pca.explained_variance_ratio_

	print variance
	print "and the cumulative variance are:"
	for i in range(len(variance)):
		print i,
		print np.sum(variance[:i+1]),
	print ""

	print "sample factor matrix:", Y1.shape
	print "gene factor matrix:", Y2.shape
	np.save("./data_inter/fm_gene_initial", Y2)







	##=============
	##==== save the Individual x Tissue matrix (with Nan in) under "./data_inter/"
	##=============
	##
	## TO use: Y1, Data_index
	##
	Data = np.zeros((K, I, D)) + float("Nan")
	for i in range(len(Data_index)):
		(tissue, pos) = Data_index[i]
		Data[tissue][pos] = Y1[i]
	print "the Tissue x Individual x Factor tensor has the dimension:",
	print Data.shape


	for d in range(D):
		m_factor = Data[:, :, d]
		np.save("./data_inter/f" + str(d) + "_tissue_indiv", m_factor)
	print "per-factor saving done..."


	##== need to save the results in tsv file (including Nan), in order to load in R
	for d in range(D):
		m_factor = np.load("./data_inter/f" + str(d) + "_tissue_indiv.npy")
		file = open("./data_inter/f" + str(d) + "_tissue_indiv.txt", 'w')
		for i in range(len(m_factor)):
			for j in range(len(m_factor[i])):
				value = m_factor[i][j]
				file.write(str(value))
				if j != len(m_factor[i])-1:
					file.write('\t')
			file.write('\n')
		file.close()



















## this script will solve the LASSO for gene fm, and provide the Beta indicator matrix for Beta LASSO to be used

## note to make files consistent with init_wl.py, both the factor matrix and the indicator matrix

## will load the saved factor matrix, and the input data X








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
from sklearn import linear_model





n_factor = 400					## TODO: tune
K = 28
D = 400							## TODO: as above




init_beta_genefm = []







if __name__ == "__main__":





	##=============
	##==== combine the indiv and tissue fm
	##=============
	factor_tissue = []
	factor_indiv = []
	for k in range(n_factor):
		#
		factor_tissue.append([])
		file = open("./data_inter/f" + str(k) + "_tissue.txt", 'r')
		while 1:
			line = (file.readline()).strip()
			if not line:
				break
			factor_tissue[-1].append(float(line))
		file.close()

		#
		factor_indiv.append([])
		file = open("./data_inter/f" + str(k) + "_indiv.txt", 'r')
		while 1:
			line = (file.readline()).strip()
			if not line:
				break
			factor_indiv[-1].append(float(line))
		file.close()

	factor_tissue = (np.array(factor_tissue)).T
	factor_indiv = (np.array(factor_indiv)).T

	print "factor tissue:",
	print factor_tissue.shape

	print "factor indiv:",
	print factor_indiv.shape

	np.save("./data_init/fm_tissue", factor_tissue)
	np.save("./data_init/fm_indiv", factor_indiv)





	##=============
	##==== build the linear system, and solve with LASSO
	##=============
	##
	## use the factor_indiv and factor_tissue to build the Y
	##
	X = []
	Y = []
	for k in range(K):
		list_pos = np.load("../preprocess/data_train/Tensor_tissue_" + str(k) + "_pos.npy")
		data = np.load("../preprocess/data_train/Tensor_tissue_" + str(k) + ".npy")

		for i in range(len(list_pos)):
			pos = list_pos[i]
			exp = data[i]

			x = np.multiply(factor_tissue[k], factor_indiv[pos])
			X.append(x)
			Y.append(exp)
	X = np.array(X)
	Y = np.array(Y)
	print "input and output of this linear system dimensions:", X.shape, Y.shape






	##=============
	##==== prepare the indicator matrix for Beta
	##=============
	##
	## input ourput: X, Y
	##
	## solve the LASSO for each gene
	####========================================================================

	#alpha = 0.1					## #0
	#alpha = 0.2					## #1
	alpha = 0.3					## #2
	#alpha = 0.5					## #3
	#alpha = 1.0					## #4




	clf = linear_model.Lasso(alpha=alpha)						## NOTE: LASSO parameter tunable
	clf.fit(X, Y)
	init_beta_genefm = clf.coef_
	print "init_beta_genefm shape:", init_beta_genefm.shape
	np.save("./data_init/fm_gene", init_beta_genefm)







	####
	##==== sparse indicator
	####
	## save non-0 genes for each factor
	init_beta_genefm = np.load("./data_init/fm_gene.npy")
	print "non-zero genes for each factor:"
	m_indi = []
	for d in range(D):
		array_factor = init_beta_genefm[:, d]
		indi_factor = np.sign(np.square(array_factor))
		m_indi.append(indi_factor)
	m_indi = np.array(m_indi)
	print m_indi.shape
	np.save("./data_temp/m_indi", m_indi)




	## check and save effective SNPs for each factor
	#
	X = np.load("../preprocess/data_train/X.npy")
	I = len(X[0])
	#
	data = np.load("../preprocess/data_train/Tensor_tissue_0.npy")
	J = len(data[0])
	#
	print "output num of active genes and num of corresponding snps in each factor:"
	mapping_cis = np.load("../preprocess/data_train/mapping_cis.npy")
	m_indi_snp = []
	for d in range(D):
		indi_snp = np.zeros(I)

		indi_factor = m_indi[d]
		for j in range(J):
			if indi_factor[j] == 1:				# gene in this factor
				start = mapping_cis[j][0]
				end = mapping_cis[j][1]
				for index in range(start, end+1):
					indi_snp[index] = 1
		print d, np.sum(indi_factor), np.sum(indi_snp)
		m_indi_snp.append(indi_snp)
	m_indi_snp = np.array(m_indi_snp)
	print m_indi_snp.shape
	np.save("./data_temp/m_indi_snp", m_indi_snp)















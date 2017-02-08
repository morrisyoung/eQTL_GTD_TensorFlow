import numpy as np
from sklearn.decomposition import PCA
import math
from sklearn import linear_model




## output:
##	Beta (from genetics to factors)


## for each factor, we use cis- SNPs of expressed genes in this factor as the input candidate SNPs, and we use LASSO


## I assume we have a subfolder under ~/GTEx_gtmnn/, and all the code and data will be cached there






X = []						# matrix of Individuals x SNPs
F = []						# factors of Individuals x D

S = 0						# num of SNPs
D = 0						# num of factors
I = 0						# num of individuals

init_beta = []





if __name__ == "__main__":




	##==== load data (simu, incomp tensor)
	X = np.load("../preprocess/data_train/X.npy")
	F = np.load("./F.npy")

	#
	I = len(X)
	S = len(X[0])
	D = len(F[0])
	print "shape:"
	print "I:", I
	print "S:", S
	print "D:", D

	#
	init_beta = np.zeros((D, S+1))




	##
	## for each factor: pick up candidate SNPs, do the LASSO
	##
	####========================================================================
	m_indi_snp = np.load("./m_indi_snp.npy")
	beta = []
	for d in range(D):
		Data = np.multiply(X, m_indi_snp[d])			# X: (n_samples, n_features)
		Target = F[:, d] 								# Y: (n_samples, n_tasks)

		clf = linear_model.Lasso(alpha=0.01)			# TODO: parameter tunable
		clf.fit(Data, Target)

		#clf.coef_							# (n_features,)
		#clf.intercept_						# value
		temp = (clf.coef_).tolist()
		temp.append(clf.intercept_)

		beta.append(temp)
	init_beta = np.array(beta)
	print "init_beta shape:",
	print init_beta.shape

	## test non-0 elements
	print "check num of non-0 snps each factor has:"
	for d in range(D):
		print d, np.sum(m_indi_snp[d]), np.sum(np.sign(np.square(init_beta[d])))
	####========================================================================






	##==== save the init
	init_beta = init_beta.T
	np.save("./Beta", init_beta)















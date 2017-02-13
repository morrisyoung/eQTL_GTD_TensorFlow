import numpy as np
from sklearn.decomposition import PCA
import math
from sklearn import linear_model









if __name__ == "__main__":



	## non-0 SNPs all factors
	init_beta = np.load("./data_init/Beta.npy")
	init_beta = init_beta[:-1]
	init_beta = init_beta.T
	print init_beta.shape
	print np.sum(np.sign(np.sum(np.square(init_beta), axis=0)))










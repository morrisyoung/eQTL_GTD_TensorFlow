##==== libraries
import math
import numpy as np
import timeit






#### simulate a full tensor + wide linear model to test (simu)
####	next: simulate a incomplete tensor + wide linear model to test (simu)
####	next: probably architect the real data (train/test), and work on real data (need to initialize first of all)



#### for now, before I resolve the large memory issue, I'll simulate a smaller model, say, 10%






##==== global variables
Y = []
T = []
U = []
V = []
alpha = 1
X = []
Beta = []
#### real data scale
'''
K = 28
I = 449
J = 19425						# num of genes
D = 400
'''
K = 28
I = 450
J = 2000
S = 244519
D = 40







def simu_Y():		# (work on global scale)
	global Y
	global T, U, V
	global K, I, J
	global D
	global alpha

	##
	U = np.expand_dims(U, axis=1)					## I x 1 x D
	print U.shape
	t_temp = np.multiply(U, V)						## I x J x D
	print t_temp.shape

	##
	Y = np.einsum('ijd,kd->kij', t_temp, T)
	print Y.shape

	##
	sigma = math.sqrt(1.0 / alpha)
	Y = np.random.normal(Y, sigma)

	return







if __name__ == "__main__":




	print "simulating..."


	##==== timer
	start_time = timeit.default_timer()



	##==============================================================================================================
	## main simu
	##==============================================================================================================
	##==== simulation
	## I will treat all observed variables as input of simu functions
	mu = 0						## TODO
	lamb = 1.0					## TODO



	##
	X = np.random.uniform(0, 2, (I, S))
	array_ones = (np.array([np.ones(I)])).T
	X = np.concatenate((X, array_ones), axis=1)								## I x (S+1)
	##
	sigma = math.sqrt(1.0 / lamb)
	Beta = np.random.normal(mu, sigma, (S+1, D))
	marker = np.random.binomial(1, 0.0001, size=(S+1, D))					## sparsity
	Beta = Beta * marker


	##
	U = np.dot(X, Beta)

	##
	T = np.random.normal(mu, sigma, (K, D))
	V = np.random.normal(mu, sigma, (J, D))

	##
	simu_Y()




	print "U:",
	print np.amax(U), np.amin(U)
	print "T:",
	print np.amax(T), np.amin(T)
	print "V:",
	print np.amax(V), np.amin(V)
	print "Beta:",
	print np.amax(Beta), np.amin(Beta)






	##
	print "T shape:", T.shape
	print "U shape:", U.shape
	print "V shape:", V.shape
	print "Beta shape:", Beta.shape
	print "Y shape:", Y.shape
	print "X shape:", X.shape


	##==== saving
	np.save("./data_simu_gtd/Y", Y)
	np.save("./data_simu_gtd/T", T)
	np.save("./data_simu_gtd/U", U)
	np.save("./data_simu_gtd/V", V)
	np.save("./data_simu_gtd/Beta", Beta)
	np.save("./data_simu_gtd/X", X)





	##################################################################
	##################################################################





	#### spreading the Y
	Y = np.load("./data_simu_gtd/Y.npy")
	data = []
	for i in range(len(Y)):
		for j in range(len(Y[i])):
			data += Y[i][j].tolist()
	data = np.array(data)
	Y_spread = data
	print Y_spread.shape
	np.save("./data_simu_gtd/Y_spread", Y_spread)






	##==== timer
	elapsed = timeit.default_timer() - start_time
	print "time spent:", elapsed











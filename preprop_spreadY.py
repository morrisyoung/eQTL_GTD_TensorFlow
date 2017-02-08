import numpy as np



K = 28
I = 0
J = 0



#### what we get:
####	Y_spread.npy
####	list_index_all.npy
####	table_index_indiv.npy
####	list_p_indiv.npy






if __name__ == "__main__":




	##==== check the individual coverage, and I
	repo_indiv = {}
	for k in range(K):
		list_pos = np.load("./Tensor_tissue_" + str(k) + "_pos.npy")
		for pos in list_pos:
			repo_indiv[pos] = 1
	print "individual coverage:", len(repo_indiv)
	print "336 is good for training data..."
	print "113 is good for testing data..."
	I = len(repo_indiv)




	##==== number of genes
	data = np.load("Tensor_tissue_0.npy")
	J = len(data[0])





	##==== fill in the spread Y
	Y = np.zeros((K, I, J))							## NOTE: it's fine to fill in Null with 0, since we won't index them at all
	for k in range(K):
		list_pos = np.load("./Tensor_tissue_" + str(k) + "_pos.npy")
		data = np.load("./Tensor_tissue_" + str(k) + ".npy")

		for i in range(len(list_pos)):
			pos = list_pos[i]
			exp = data[i]
			Y[k][pos] = exp
	Y_spread = np.reshape(Y, -1)
	print Y_spread.shape
	np.save("./Y_spread", Y_spread)







	##==== build the individual indexing
	##
	repo_tissue_indiv = {}
	repo_indiv_tissue = {}
	for k in range(K):
		list_pos = np.load("./Tensor_tissue_" + str(k) + "_pos.npy")
		repo_tissue_indiv[k] = np.sort(list_pos)

		#
		for pos in list_pos:
			if pos in repo_indiv_tissue:
				repo_indiv_tissue[pos].append(k)
			else:
				repo_indiv_tissue[pos] = [k]
	list_all = []
	for k in range(K):
		for indiv in repo_tissue_indiv[k]:
			list_all += (np.arange(J) + k*I*J + indiv*J).tolist()
	list_all = np.array(list_all)
	np.save("./list_index_all", list_all)


	##
	repo_indiv_index = {}
	for i in range(I):
		list_temp = []
		for k in repo_indiv_tissue[i]:
			list_temp += (np.arange(J) + k*I*J + i*J).tolist()
		repo_indiv_index[i] = list_temp
	table_index_indiv = []
	for i in range(I):
		table_index_indiv.append(repo_indiv_index[i])
	table_index_indiv = np.array(table_index_indiv)
	np.save("./table_index_indiv", table_index_indiv)


	##
	list_p = []
	for i in range(I):
		list_p.append(len(repo_indiv_tissue[i]))
	list_p = np.array(list_p) * 1.0
	list_p = list_p / np.sum(list_p)
	np.save("./list_p_indiv", list_p)















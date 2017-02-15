import numpy as np


## extract the (k, indiv) in order


K = 28



if __name__ == "__main__":



	##==== build the individual indexing
	list_pos_all = []
	for k in range(K):
		list_pos = np.load("./Tensor_tissue_" + str(k) + "_pos.npy")
		list_pos = np.sort(list_pos)

		for pos in list_pos:
			list_pos_all.append((k, pos))
	list_pos_all = np.array(list_pos_all)
	print list_pos_all.shape
	np.save("./list_pos_all", list_pos_all)




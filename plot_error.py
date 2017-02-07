import matplotlib.pyplot as plt
import numpy as np





def load_txt(filename):
	file = open(filename, 'r')
	arr = []
	while 1:
		line = (file.readline()).strip()
		if not line:
			break

		value = float(line)
		arr.append(value)
	arr = np.array(arr)
	return arr




if __name__=="__main__":



	##==== total likelihood
	#arr = np.load("./result/loglike_total.npy")





	arr = load_txt("./result/list_error.txt")





	print len(arr)
	plt.plot(arr[:], 'r')


	plt.xlabel("Number of iterations")
	plt.ylabel("Total squared error")
	#plt.title("Joint Log Likelihood during Model Training")
	plt.grid()
	plt.show()







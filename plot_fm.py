import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
import sys





if __name__== "__main__":


	filename = sys.argv[1]
	#fm_loading = np.load('result/data_pde_2_800.npy')
	fm_loading = np.load(filename)



	sns.set(context="paper", font="monospace")
	f, ax = plt.subplots(figsize=(22, 19))	# TODO
#	f, ax = plt.subplots(figsize=(26, 9))


	#sns_plot = sns.heatmap(fm_loading, xticklabels=x_label, yticklabels=y_label)
	sns_plot = sns.heatmap(fm_loading)
	#sns_plot = sns.heatmap(fm_loading, yticklabels=y_label)
	ax.set_xlabel('Factors')
	ax.set_ylabel('Individuals')			# TODO
#	plt.yticks(rotation=0)
	plt.show()

	fig = sns_plot.get_figure()
	#fig.savefig("plot/quantile_c22_gene.jpg")
	#fig.savefig("/Users/shuoyang/Desktop/fm_gene.jpg")
	#fig.savefig("/Users/shuoyang/Desktop/fm_heatmap.jpg")


	print "done..."







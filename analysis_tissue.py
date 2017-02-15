import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
import sys
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist




## func:
##	plot tissue fm
##	hierarchical clustering tissues




list_chr_color = ['k', '#988ED5', 'm', '#8172B2', '#348ABD', '#EEEEEE', '#FF9F9A', '#56B4E9', '#8C0900', '#6d904f', 'cyan', 'red', 'g', '#C4AD66', '#6ACC65', 'gray', '#F0E442', '#017517', '#B0E0E6', '#eeeeee', '#55A868', '0.70']




if __name__ == "__main__":




	list_tissues = np.load("./data_real/Tissue_list.npy")




	################################################################################
	#### plot the tissue fm
	################################################################################
	'''
	fm_loading = np.load("./result/T.npy")
	threshold_factor = 50
	fm_loading = fm_loading[:,:threshold_factor]


	sns.set(context="paper", font="monospace")
	f, ax = plt.subplots(figsize=(22, 19))		# TODO


	sns_plot = sns.heatmap(fm_loading, xticklabels=np.arange(threshold_factor), yticklabels=list_tissues)
	#sns_plot = sns.heatmap(fm_loading)
	#sns_plot = sns.heatmap(fm_loading, yticklabels=y_label)
	ax.set_xlabel('Factors')
	ax.set_ylabel('Tissues')
#	plt.yticks(rotation=0)
	plt.show()

	#fig = sns_plot.get_figure()
	#fig.savefig("plot/quantile_c22_gene.jpg")
	#fig.savefig("/Users/shuoyang/Desktop/fm_gene.jpg")
	#fig.savefig("/Users/shuoyang/Desktop/fm_heatmap.jpg")
	'''







	################################################################################
	#### plot the tissue fm
	################################################################################
	fm_loading = np.load("./result/T.npy")
	X = fm_loading
	print X.shape


	## NOTE: the clustering method
	# generate the linkage matrix
	Z = linkage(X, 'weighted')
	print Z.shape


	# calculate full dendrogram
	fig = plt.figure(figsize=(15, 15))
	#plt.figure()
	plt.title('hierarchical clustering of tissue activations of different factors')
	plt.xlabel('tissues')
	plt.ylabel('distance (Euclidean)')
	dendrogram(
	    Z,
	    leaf_rotation=90.,  # rotates the x axis labels
	    leaf_font_size=12.,  # font size for the x axis labels
	    labels = list_tissues,
	)
	plt.show()
	#plt.savefig("/Users/shuoyang/Desktop/d" + str(d) + ".png")
	#plt.close(fig)















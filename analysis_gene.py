#import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
import sys
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist




list_chr_color = ['k', '#988ED5', 'm', '#8172B2', '#348ABD', '#EEEEEE', '#FF9F9A', '#56B4E9', '#8C0900', '#6d904f', 'cyan', 'red', 'g', '#C4AD66', '#6ACC65', 'gray', '#F0E442', '#017517', '#B0E0E6', '#eeeeee', '#55A868', '0.70']





if __name__ == "__main__":




	list_genes = np.load("./data_real/Gene_list.npy")




	################################################################################
	#### plot the fm
	################################################################################
	"""
	fm_loading = np.load("./result/V.npy")
	#threshold_factor = 50
	#fm_loading = fm_loading[:, :threshold_factor]


	## TEST range
	## seems [-1500, 1500] is good enough
	#print np.sort(np.reshape(fm_loading, -1))[:10]
	#print np.sort(np.reshape(fm_loading, -1))[-10:-1]


	sns.set(context="paper", font="monospace")
	f, ax = plt.subplots(figsize=(22, 19))		# TODO


	#sns_plot = sns.heatmap(fm_loading, xticklabels=np.arange(len(fm_loading[0])), yticklabels=list_genes, vmin=-1500, vmax=1500)
	sns_plot = sns.heatmap(fm_loading, xticklabels=np.arange(len(fm_loading[0])), yticklabels=list_genes)
	#sns_plot = sns.heatmap(fm_loading)
	#sns_plot = sns.heatmap(fm_loading, yticklabels=y_label)
	ax.set_xlabel('Factors')
	ax.set_ylabel('Genes')
	#plt.yticks(rotation=0)
	#plt.show()

	fig = sns_plot.get_figure()
	#fig.savefig("plot/quantile_c22_gene.jpg")
	#fig.savefig("/Users/shuoyang/Desktop/fm_gene.jpg")
	fig.savefig("/Users/shuoyang/Desktop/fm_heatmap.jpg")
	"""






	################################################################################
	#### Manhhatan
	################################################################################
	##====
	fm_loading = np.load("./result/V.npy")

	## range test
	print np.sort(np.reshape(fm_loading, -1))[:10]
	print np.sort(np.reshape(fm_loading, -1))[-10:-1]

	list_num_gene = np.load("./data_real/list_num_gene.npy")
	for d in range(len(fm_loading[0])):
		print d

		beta = fm_loading[:, d]
		fig = plt.figure()
		start = 0
		for i in range(22):
			num = list_num_gene[i]
			color = list_chr_color[i]
			plt.plot(np.arange(start, start+num), beta[start: start+num], 'o', color = color, alpha=0.5)
			#ax.stem(np.arange(start, start+num), beta[start: start+num], 'o', color = color, alpha=0.5)
			start += num
		#plt.axis([0, len(beta), -0.20, 0.20])				# NOTE: manually test the range of the veta values
		plt.grid(True)
		plt.title("factor#" + str(d))
		plt.xlabel("gene index")
		plt.ylabel("beta of genes")
		#plt.savefig("/Users/shuoyang/Desktop/figs_snpbeta/d" + str(d) + ".png")
		plt.show()
		plt.close(fig)











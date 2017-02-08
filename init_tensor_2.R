## do incomplete PCA for each element of the (factor x Tissue x Individual) tensor
## dir: "./data_inter/" or "./data_simu_inter/" (cluster) and "./data_temp/" (local)
## remove all local data afterwards


library(pcaMethods)
n_factor <- 400  # TODO
for (k in 0:(n_factor-1)){
  print(paste("Working on factor #", k))
  data = read.table(paste("./data_temp/f", toString(k), "_tissue_indiv.txt", sep=""))
  data[data=="NaN"] <- NA
  pc <- pca(data, nPcs=1, method="ppca")  # TODO
  loading <- loadings(pc)
  score <- scores(pc)
  # Individual
  write.table(loading, file=paste("./data_temp/f", toString(k), "_indiv.txt", sep=""), sep="\t", col.names = FALSE, row.names = FALSE)
  # Tissue
  write.table(score, file=paste("./data_temp/f", toString(k), "_tissue.txt", sep=""), sep="\t", col.names = FALSE, row.names = FALSE)
}



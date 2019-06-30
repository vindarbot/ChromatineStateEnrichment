library(tidyverse)
library(igraph)
library(ggplot2)

matrix <- read.csv('matrix.txt',sep="\t",head=T)


matrix <- matrix[,1:ncol(matrix)-1]

names <- combn(names(matrix[-1]), 2)

freq <- combn(matrix[-1], 2, function(x) sum(x[1] * x[2]))

matrix_adj <- data.frame(col1 = names[1,], col2 = names[2,], freq = freq)


g <- graph.data.frame(matrix_adj)

netm <- get.adjacency(g,attr='freq',sparse = F)

palf <- colorRampPalette(c("white", "dark red")) 



png(filename="images/matrix.png",height=800,width=1000,res=120)
heatmap(netm, Rowv = NA, Colv = NA, col = palf(100), 
        
        scale="none", margins=c(10,10) )
dev.off()


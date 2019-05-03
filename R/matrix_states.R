dir <- rstudioapi::getSourceEditorContext()$path

setwd('~/Desktop/Chromatine_states/')
matrix <- read.csv('results/matrix.txt',sep="\t", head=T)


matrix['X1']

for (i in 1:36) {
  print(sum(matrix[i]))
}
sum(matrix['X1'])


for (i in 1:36) {
  print(as.integer(i))
}
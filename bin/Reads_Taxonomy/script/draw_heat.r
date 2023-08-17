args <- commandArgs(TRUE)
    if (length(args) != 2){
                print("Example : Rscript draw_heat.r expre.xls heatmap.pdf")
                q()
        }

library(pheatmap)
data <- read.csv(args[1],sep='\t',header=T,row.names=1)
data[data==0]=0.0001
log_data <- log10(data)
pdf(args[2],w=12,h=12)
pheatmap::pheatmap(log_data,color=colorRampPalette(c("white","yellow","red"))(100),treeheight_row=10, treeheight_col=10,cluster_rows = T,cluster_columns = T)
dev.off()

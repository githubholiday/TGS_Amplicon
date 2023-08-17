args <- commandArgs(TRUE)
    if (length(args) != 3){
                print("Example : inputfile out.pdf type")
                q()
        }
library(ggplot2)
library(data.table)
library(reshape2)
data <- read.csv(args[1],sep='\t')
if(args[3]=="T"){
    data_t <- data[,1:3]
    data_t
    names(data_t) <- c("sample","species","count")
    types = "species"
}else{
types <- names(data)[1]
data_t <- melt(data,id=1)
names(data_t) <- c("species","sample","count")
}
#n=c('#004DA1','#F7CA18','#4ECDC4','#F9690E','#B35AA5','#7DCDF3','#0080CC','#F29F41','#DE6298','#C4EFF6','#C8F7C5','#FCECBB','#F9B7B2','#E7C3FC','#81CFE0','#BDC3C7','#EDC0D3','#E5EF64','#4ECDC4','#168D7C','#103652','#D2484C','#E79D01')
spe_length = ceiling(length(unique(data_t$species))/15)
sam_length = length(unique(data_t$sample))
#pdf(args[2],width = figwidth)
figwidth = spe_length*2.3+sam_length*0.3
figwidth
pdf(args[2],width = figwidth)
ggplot(data_t,aes(sample,count,fill=species))+
      geom_bar(stat="identity",position="fill")+
      scale_y_continuous(labels = scales::percent)+
      labs(y='Absolute Abundance(%)')+
      guides(fill=guide_legend(title = types))+
#      theme(axis.text.x = element_text(angle = 90, hjust = 1))
      theme(axis.text.x = element_text(angle = 90, hjust = 1),panel.background = element_blank(),axis.ticks.x = element_blank())
dev.off()

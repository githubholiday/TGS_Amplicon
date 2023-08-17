args <- commandArgs(TRUE)
    if (length(args) != 2){
		print("Example : inputfile out.stat.xls")
		q()
	}

library(vegan)
data<- read.table(args[1],row.name=1,head=T,sep="\t",quote = "",comment.char = "")

data_t <- t(data)
if (length(rownames(data_t)) < 2){
    print("样本数量过少，少于2个，不计算alpha多样性指标")
    q()
}


shannon <- diversity(data_t, index = "shannon")
simpson <- diversity(data_t, index = "simpson")
invsimpson <- diversity(data_t, index = "inv")
observed_species <- specnumber(data_t)
chao1 <- estimateR(data_t)[2,]
ACE <- estimateR(data_t)[4,]
pielou <- diversity(data_t,index = "shannon")/log(specnumber(data_t),exp(1))
final <- data.frame(chao1,ACE,observed_species,pielou,shannon,simpson)
write.table(round(final,2),args[2],col.names=T, row.names=T,quote=F,sep="\t")

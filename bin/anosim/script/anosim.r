#!/annoroad/data1/bioinfo/PROJECT/RD/Cooperation/RD_Group/yangzhang/miniconda3/envs/amplified_pipeline/bin/Rscript
#作者：张阳
#邮箱：yangzhang@genome.cn
#时间：2023年05月10日 星期三 15时43分09秒
#版本：v0.0.1
#用途：用于anosim分析，判断分组合理性
library(getopt)
para<- matrix(c(
    'help',    'h',    0,  "logical",
    'infile',   'i',    1,  "character",
    'cmp',   'c',    1,  "character",
    'outdir',   'o',    1,  "character"
),byrow=TRUE,ncol=4)
opt <- getopt(para,debug=FALSE)
print_usage <- function(para=NULL){
    cat(getopt(para,usage=TRUE))
    cat("
    Options:
    help    h   NULL        get this help
    infile  i   character   merge.qiime.xls , 物种丰度文件，列为样本，行为物种名称，值为丰度
    cmp  c character cmp.list,要求只有两列，tab分隔，第一列为Sample，第二列为Group，大小写也需要符合
    outdir  o character , 结果输出路径
    \n")
    q(status=1)
}
if (is.null(opt$infile)) {print_usage(para)}
library(vegan)
library(ggplot2)
library(dplyr)
library(ggsci)
colors = c(pal_aaas("default", alpha = 0.8)(10),pal_lancet("lanonc", alpha = 0.8)(9),pal_nejm("default", alpha = 0.8)(8),pal_jama("default", alpha = 0.8)(7),pal_jco("default", alpha = 0.8)(10))
infile = opt$infile # "merge.qiime.xls"
outdir = opt$outdir # 
cmp = opt$cmp # cmp.list 要求只有两列，tab分隔，第一列为Sample，第二列为Group，大小写也需要符合。
# 读取物种丰度文件
c = read.table(infile , sep = "\t", quote = "")
a = t(c)
dat = as.data.frame(a[2:nrow(a),2:ncol(a)])
dat = as.data.frame(lapply(dat,as.numeric))
rownames(dat)=a[,1][2:length(a[,1])]
colnames(dat)=a[1,][2:length(a[1,])]
# 读取分组文件
tmp = as.data.frame(rownames(dat))
colnames(tmp) = "Sample"
group = read.table( cmp , sep="\t" , header=T) 
real_group = merge(tmp,group,sort=F)[,"Group"]
group_name = sort(real_group[!duplicated(real_group)])
# 进行Anosim分析
out_data=data.frame("group"=0,"R"=0,"p"=0)
anosim=anosim(dat, real_group, permutations=999)
summary(anosim)
par(mar=c(5,5,5,5))
result=paste("R=",round(anosim$statistic,3),"    p=", round(anosim$signif,3))
mycol=colors[1:(length(group_name)+1)]
pdf(paste(outdir,"/anosim.all.pdf",sep='') , width=10 , height=8)
boxplot(anosim$dis.rank~anosim$class.vec, pch="+", col=mycol, range=1, boxwex=0.5, notch=TRUE, xlab = "" , ylab="Bray-Curtis Rank", main="Bray-Curtis Anosim", sub=result)
dev.off()
out_data[1,] = c("all",round(anosim$statistic,3), round(anosim$signif,3))

combine = combn(group_name,2)
for (i in 1:ncol(combine)){
    samples = group[which(group$Group == combine[1,i] | group$Group == combine[2,i]),]
    samples
    dat_tmp = dat[rownames(dat)  %in%  samples$Sample,]
    b_tmp = data.frame(dat_tmp)
    b_tmp$Sample = rownames(dat_tmp)
    group_tmp = merge(b_tmp,samples,sort=F)[,"Group"]
    dim(dat_tmp)
    dim(group_tmp)
    anosim_tmp = anosim(dat_tmp, group_tmp, permutations=999)
    par(mar = c(5,5,5,5))
    result_tmp = paste("R=",round(anosim_tmp$statistic,3),"    p=", round(anosim_tmp$signif,3))
    pdf(paste(outdir,"/anosim.",combine[1,i],"-",combine[2,i],".pdf",sep=''), width=10 , height=8)
    mycol=colors[1:3]
    boxplot(anosim_tmp$dis.rank~anosim_tmp$class.vec, pch="+", col=mycol, range=1, boxwex=0.5, notch=TRUE, xlab = "" ,ylab="Bray-Curtis Rank", main="Bray-Curtis Anosim", sub=result_tmp)
    dev.off()
    out_data[i+1,] = c(paste(combine[1,i],"-",combine[2,i],sep=''),round(anosim_tmp$statistic,3), round(anosim_tmp$signif,3))
}
write.table(out_data,file=paste(outdir,"/anosim.stat.xls",sep=''),sep="\t",row.names=F,quote=F)


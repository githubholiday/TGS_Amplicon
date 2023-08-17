#!/annoroad/data1/bioinfo/PROJECT/RD/Cooperation/RD_Group/yangzhang/miniconda3/envs/amplified_pipeline/bin/Rscript
#作者：张阳
#邮箱：yangzhang@genome.cn
#时间：2023年05月10日 星期三 15时43分09秒
#版本：v0.0.1
#用途：用于绘制 物种累积曲线 allsample.accumulation.curve.pdf
library('getopt')
library(vegan)
library(ggplot2)

para<- matrix(c(
    'help',    'h',    0,  "logical",
    'infile',   'i',    1,  "character",
    'outfile',   'o',    1,  "character"
),byrow=TRUE,ncol=4)
opt <- getopt(para,debug=FALSE)
print_usage <- function(para=NULL){
    cat(getopt(para,usage=TRUE))
    cat("
    Options:
    help    h   NULL        get this help
    infile  i   character   merge.qiime.xls , 物种丰度文件，列为样本，行为物种名称，值为丰度
    outfile  o character allsample.accumulation.curve.pdf, 物种累积曲线结果图
    \n")
    q(status=1)
}
if (is.null(opt$infile)) {print_usage(para)}

infile = opt$infile # "merge.qiime.xls"
outfile = opt$outfile # "allsample.accumulation.curve.pdf"

c = read.table(infile , header = T, sep = "\t", quote = "", row.names = 1)
a = t(c)
sp = specaccum(a, "random")
pdf(outfile , width = 10, height = 8)
plot(sp, ci.type="poly", col="blue", lwd=2, ci.lty=0, ci.col="lightblue" ,xlab="sample number", ylab="specise number")
#boxplot(sp, col="yellow", add=TRUE, pch="+")
dev.off()
#!/annoroad/data1/bioinfo/PROJECT/RD/Cooperation/RD_Group/yangzhang/miniconda3/envs/amplified_pipeline/bin/Rscript
#作者：张阳
#邮箱：yangzhang@genome.cn
#时间：2023年05月10日 星期三 15时43分09秒
#版本：v0.0.1
#用途：用于绘制 稀释性曲线 allsample.rarefaction.curve.pdf
library(getopt)
library(vegan)
library(ggplot2)
library(doBy)

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
    outfile  o character allsample.rarefaction.curve.pdf, 稀释性曲线结果图
    \n")
    q(status=1)
}
if (is.null(opt$infile)) {print_usage(para)}

infile = opt$infile # "merge.qiime.xls"
outfile = opt$outfile # "allsample.rarefaction.curve.pdf"

c = read.table(infile , header = T, sep = "\t", quote = "", row.names = 1)
a = t(c)
min(rowSums(a))
color = c('red', 'green', 'blue', 'orange')
pdf(outfile , width = 10, height = 8)
rarecurve(a, step = 500, xlab="Number of sequence", ylab = "Species number ", col = color ,label=FALSE) 
legend("right", legend=rownames(a) , col=color , lty=1 , lwd=2)
dev.off()


# #计算多种 Alpha 多样性指数，结果返回至向量
# alpha_index <- function(x, method = 'richness', tree = NULL, base = exp(1)) {
#   if (method == 'richness') result <- rowSums(x > 0)    #丰富度指数
#   else if (method == 'chao1') result <- estimateR(x)[3, ]    #Chao1 指数
#   else if (method == 'ace') result <- estimateR(x)[5, ]    #ACE 指数
#   else if (method == 'shannon') result <- diversity(x, index = 'shannon', base = base)    #Shannon 指数
#   else if (method == 'simpson') result <- diversity(x, index = 'simpson')    #Gini-Simpson 指数
#   else if (method == 'pielou') result <- diversity(x, index = 'shannon', base = base) / log(estimateR(x)[1, ], base)    #Pielou 均匀度
#   else if (method == 'gc') result <- 1 - rowSums(x == 1) / rowSums(x)    #goods_coverage
#   else if (method == 'pd' & !is.null(tree)) {    #PD_whole_tree
#     pd <- pd(x, tree, include.root = FALSE)
#     result <- pd[ ,1]
#     names(result) <- rownames(pd)
#   }
#   result
# }

# #根据抽样步长（step），统计每个稀释梯度下的 Alpha 多样性指数，结果返回至列表
# alpha_curves <- function(x, step, method = 'richness', rare = NULL, tree = NULL, base = exp(1)) {
#   x_nrow <- nrow(x)
#   if (is.null(rare)) rare <- rowSums(x) else rare <- rep(rare, x_nrow)
#   alpha_rare <- list()
  
#   for (i in 1:x_nrow) {
#     step_num <- seq(0, rare[i], step)
#     if (max(step_num) < rare[i]) step_num <- c(step_num, rare[i])
    
#     alpha_rare_i <- NULL
#     for (step_num_n in step_num) alpha_rare_i <- c(alpha_rare_i, alpha_index(x = rrarefy(x[i, ], step_num_n), method = method, tree = tree, base = base))
#     names(alpha_rare_i) <- step_num
#     alpha_rare <- c(alpha_rare, list(alpha_rare_i))
#   }
  
#   names(alpha_rare) <- rownames(x)
#   alpha_rare
# }
# ################Richness指数曲线   重复抽样 5 次###########
# ##多计算几次以获取均值 ± 标准差，然后再展示出也是一个不错的选择
# otu=a
# plot_richness <- data.frame()

# for (n in 1:5) {
#   richness_curves <- alpha_curves(otu, step = 2000, method = 'richness')
  
#   for (i in names(richness_curves)) {
#     richness_curves_i <- (richness_curves[[i]])
#     richness_curves_i <- data.frame(rare = names(richness_curves_i), alpha = richness_curves_i, sample = i, stringsAsFactors = FALSE)
#     plot_richness <- rbind(plot_richness, richness_curves_i)
#   }
# }

# #计算均值 ± 标准差（doBy 包中的 summaryBy() 函数）

# plot_richness_stat <- summaryBy(alpha~sample+rare, plot_richness, FUN = c(mean, sd))
# plot_richness_stat$rare <- as.numeric(plot_richness_stat$rare)
# plot_richness_stat[which(plot_richness_stat$rare == 0),'alpha.sd'] <- NA

# #ggplot2 作图，可自行修改 ggplot2 作图细节
# p1<-ggplot(plot_richness_stat, aes(rare, alpha.mean, color = sample)) +
#   geom_line() +
#   geom_point() +
# #   geom_errorbar(aes(ymin = alpha.mean - alpha.sd, ymax = alpha.mean + alpha.sd), width = 500) +
#   labs(x = 'Number of sequences', y = 'Richness', color = NULL) +
#   theme(panel.grid = element_blank(), panel.background = element_rect(fill = 'transparent', color = 'black'), legend.key = element_rect(fill = 'transparent')) +
#   geom_vline(xintercept = min(rowSums(otu)), linetype = 2) +
#   scale_x_continuous(breaks = seq(0, 30000, 5000), labels = as.character(seq(0, 30000, 5000)))
# ggsave(outfile,p1,width=10,height=8)



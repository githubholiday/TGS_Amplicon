#!/annoroad/data1/bioinfo/PROJECT/RD/Cooperation/RD_Group/yangzhang/miniconda3/envs/amplified_pipeline/bin/Rscript
#作者：张阳
#邮箱：yangzhang@genome.cn
#时间：2023年05月10日 星期三 15时43分09秒
#版本：v0.0.1
#用途：用于绘制 等级丰度曲线 allsample.rank.curve.pdf
library('getopt')
para<- matrix(c(
    'help',    'h',    0,  "logical",
    'infile',   'i',    1,  "character",
    'scriptdir',   's',    1,  "character",
    'outfile',   'o',    1,  "character"
),byrow=TRUE,ncol=4)
opt <- getopt(para,debug=FALSE)
print_usage <- function(para=NULL){
    cat(getopt(para,usage=TRUE))
    cat("
    Options:
    help    h   NULL        get this help
    infile  i   character   merge.qiime.xls , 物种丰度文件，列为样本，行为物种名称，值为丰度
    scriptdir  s character rankabundance.R 所在路径
    outfile  o character allsample.rank.curve.pdf, 等级丰度曲线结果图
    \n")
    q(status=1)
}
if (is.null(opt$infile)) {print_usage(para)}

infile = opt$infile # "merge.qiime.xls"
outfile = opt$outfile # "allsample.rank.curve.pdf"
scriptdir = opt$scriptdir # rankabundance.R 所在路径

# library(BiodiversityR)  #BiodiversityR 包 rankabundance() 实现 OTU 排序 # 安装不成功 所以直接用函数吧~~
source(paste(scriptdir,"/rankabundance.R",sep=''))
library(ggplot2)  #作图

otu <- read.delim(infile , row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE)
otu=t(otu)
otu_relative <- otu / rowSums(otu)	#转化为相对丰度
rank_dat <- data.frame()
for (i in rownames(otu_relative)) {
  rank_dat_i <- data.frame(rankabundance(subset(otu_relative, rownames(otu_relative) == i), digits = 6))[1:2]
  rank_dat_i$sample <- i
  rank_dat <- rbind(rank_dat, rank_dat_i)
}
rank_dat <- subset(rank_dat, abundance != 0)
p<-ggplot(rank_dat, aes(rank, log(abundance, 10), color = sample)) +
  geom_line() +
  labs(x = 'Species rank', y = 'Relative adundance ', color = NULL) +
  theme(panel.grid = element_blank(), panel.background = element_rect(fill = 'transparent', color = 'black'), legend.key = element_rect(fill = 'transparent'),legend.position = 'none') + #如果需要标签，则把这个position的信息去掉。目前为不加标签
  scale_y_continuous(breaks = 0:-7, labels = expression(10^0, 10^-1, 10^-2 ,10^-3, 10^-4, 10^-5, 10^-6, 10^-7), limits = c(-7, 0))

ggsave(outfile , p )


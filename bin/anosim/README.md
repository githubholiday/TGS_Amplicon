### 模块： mk_anosim

*模块功能：用于anosim检验分析，判断分组合理性
*模块版本：v1.0.0
*邮箱： yangzhang@genome.cn

### 使用示例及参数说明：

Usage:
	 make -f mk_anosim infile= outdir= cmp= software= anosim
参数说明：
	 software: [文件|可选]  模块配置文件，和软件相关参数，默认为.//software/software.txt 
	 infile: [文件|必需]  输入文件，物种丰度文件，例如：merge.qiime.xls、otu.xls
	 outdir: [路径|必需]  分析结果输出路径 
	 cmp: [文件|必需]  cmp.list, 要求有两列，tab分隔，Sample和Group，大小写需要符合 

### 输入文件示例
见test/input/
.
├── cmp.list
└── merge.qiime.xls

### 运行环境及软件：
	北京238 R 4.2.3 (vegan,dplyr,ggplot2,ggsci,getopt)

### 资源消耗及运行时长
	1CPU, 5G , 2min

### 输出文件示例
.
├── anosim.A-B.pdf          A-B组的anosim检验结果
├── anosim.A-C.pdf          A-C组的anosim检验结果
├── anosim.all.pdf          所有组的anosim检验结果
├── anosim.B-C.pdf          B-C组的anosim检验结果
└── anosim.stat.xls         以上所有情况的anosim检验结果的R,p值汇总表格

主要结果文件说明：
（1）anosim*pdf
横坐标中Between代表组间，其他代表各自的分组；纵坐标代表距离的排名（数值越小代表距离越近）
（2）anosim.stat.xls
R：差异程度，一般介于（0，1）之间。
R>0，说明组间存在差异（R>0.75：大差异；R>0.5：中等差异，R>0.25：小差异）；
R=0或在0附近，表明组间没有差异；
若R出现<0的情况，说明组内差异显著大于组间差异，这个时候表明分组或采样不合理，需要重做实验。
P：P值，数值小于0.05、0.01或在两者范围内，表明分组有显著性差异，进而反映出目标分组有意义。

### 注意事项
Anosim分析（Analysis of similarities）是一种基于置换检验和秩和检验的非参数检验方法，用来检验组间的差异是否显著大于组内差异，从而判断分组是否有意义。Anosim分析使用距离进行分析，默认为method="bray"，（本分析选择的是默认的bray），可以选择其他距离（和vegdist()函数相同）。

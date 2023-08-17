### 模块： mk_PCoA

*模块功能：PCoA分析
*模块版本：v1.0.0
*邮箱： yangzhang@genome.cn

### 使用示例及参数说明：

Usage:
	 make -f mk_PCoA infile= cmp= method= outfile1= outfile2= outfile3= outdir= software= PCoA
参数说明：
	 software: [文件|可选]  模块配置文件，和软件相关参数，默认为.//software/software.txt 
	 infile: [文件|必需]  输入文件，物种丰度文件，如merge.qiime.xls，列为样本，行为物种名称，值为丰度
	 cmp: [文件|必需]  输入文件，如cmp.list，要求只有两列，tab分隔，第一列为Sample，第二列为Group，大小写也需要符合。
	 method: [文件|必需] 计算距离矩阵的方法，可选有：manhattan,euclidean,canberra,bray,kulczynski,jaccard,gower,altGower,morisita,horn,mountford,raup,binomial,chao,cao,mahalanobis。具体可以查看vegan包的说明（函数为vegdist），在三代扩增子分析中选择的是 bray 和 jaccard
	 outfile1: [文件|必需]  输出文件，PCoA结果图。如PCoA_ellipse_jaccard.pdf，建议在文件名中增加方法，如jaccard，便于进行区分
	 outfile2: [文件|必需]  输出文件，PCoA结果图画图用的表格。如PCoA_jaccard.xls，建议在文件名中增加方法，如jaccard，便于进行区分
	 outfile3: [文件|必需]  输出文件，PCoA结果图各个轴的解释结果。如PCoA_axis_jaccard.xls，建议在文件名中增加方法，如jaccard，便于进行区分
	 outdir: [路径|必需]   输出路径

### 输入文件示例
见test/input/
.
├── cmp.list
└── merge.qiime.xls

### 运行环境及软件：
	北京238 R 4.2.3 (vegan,ape,dplyr,ggplot2,ggsci)

### 资源消耗及运行时长
	申请CPU：1
	申请内存：1G
	运行时长：1min

### 输出文件示例
.
├── PCoA_axis_bray.xls       PCoA结果图各个轴的解释结果
├── PCoA_bray.xls            PCoA结果图画图用的表格
└── PCoA_ellipse_bray.pdf    PCoA结果图

主要结果文件说明：
（1）PCoA_ellipse*.pdf：
图中每个点代表一个样品；不同颜色代表不同分组；椭圆形圈表示其为95%置信椭圆(即该样本组假如有100个样本会有95个落在其中)。横坐标表示第一主成分，百分比则表示第一主成分对样品差异的贡献值；纵坐标表示第二主成分，百分比表示第二主成分对样品差异的贡献值。
（2）PCoA*.xls：
Sample：样本
bac_PCo1：第一主成分坐标
bac_PCo2：第二主成分坐标
Group：分组
（3）PCoA_axis*.xls
axis：axis number.
Eigenvalues：All eigenvalues (positive, null, negative).所有特征值
Relative_eig：Relative eigenvalues.相对特征值(每个轴的解释量)
Broken_stick：Expected fractions of variance under the broken stick model.断棒模型下的预期方差分数
Cumul_eig：Cumulative relative eigenvalues.累积相对特征值
Cumul_br_stick：Cumulative broken stick fractions.累计断棒分数
### 注意事项
ape官网说明：https://rdrr.io/cran/ape/man/pcoa.html
### 模块： mk_Network

*模块功能：Network图绘制
*模块版本：v1.0.0
*邮箱： yangzhang@genome.cn

### 使用示例及参数说明：

Usage:
	 make -f mk_Network infile= outfile1= outfile2= outdir= software= Network
参数说明：
	 software: [文件|可选]  模块配置文件，和软件相关参数，默认为.//software/software.txt 
	 infile: [文件|必需]  输入文件，物种丰度文件，如merge.qiime.xls，列为样本，行为物种名称，值为丰度
	 threshold: [字符|可选]  筛选阈值，默认0.6
	 outfile1: [文件|必需]  输出文件，Network.edge.csv, 网络图的边结果
	 outfile2: [文件|必需]  输出文件，Network.pdf, 网络图
	 outdir: [路径|必需]   输出路径 

### 输入文件示例
见test/input/
.


### 运行环境及软件：
	北京238 R 4.2.3 (reshape2,igraph)

### 资源消耗及运行时长
	申请CPU：1
	申请内存：1G
	运行时长：1min

### 输出文件示例
Network.edge.xls:
（1）Source：第一个节点名称；
（2）Target：第二个节点名称；
（3）weight为两个节点的相关性，绝对值越大相关性越强，正值表示正相关，负值表示负相关。

Network.p*:
圈的大小代表该物种在所有样本中都检出的总次数，圈越大，表示检测到该物种的样本越多，反之圈越小，表示检测到该物种的样本越少。
线条的粗细代表两个物种间的相关性大小（相关系数绝对值），相关性越大，线条越粗，相关性越小，线条越细。

主要结果文件说明：
网络图是相关性分析的一种表现形式，根据各个物种在各个样品中的丰度以及变化情况，进行皮尔森相关系数( pearson )分析，用cutoff＝0.6对相关系数的绝对值进行过滤，构建相关性网络。基于网络图的分析，可以获得物种的共存关系，得到物种在同一环境下的相互作用的情况。网络通常由边和节点构成，一条边由两个节点连接而成，边属性统计结果见下表。

### 注意事项

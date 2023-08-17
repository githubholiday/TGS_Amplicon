### 模块： mk_alpha

*模块功能：绘制α多样性曲线（rank：等级丰度曲线；rarefaction：稀释性曲线；accumulation：物种累积曲线）
*模块版本：v1.0.0
*邮箱： yangzhang@genome.cn

### 使用示例及参数说明：

Usage:
	 make -f mk_alpha infile= outdir= outfile= software= rank
	 make -f mk_alpha infile= outdir= outfile= software= rarefaction
	 make -f mk_alpha infile= outdir= outfile= software= accumulation
Target说明：
	rank:等级丰度曲线
	rarefaction:稀释性曲线
	accumulation:物种累积曲线图
参数说明：
	 software: [文件|可选]  模块配置文件，和软件相关参数，默认为.//software/software.txt 
	 infile: [文件|必需]  输入文件，物种丰度文件，例如：merge.qiime.xls、otu.xls
	 outdir: [路径|必需]  分析结果输出路径 
	 outfile: [文件|必需]  分析结果文件名 allsample.rank.curve.pdf; allsample.rarefaction.curve.pdf;allsample.accumulation.curve.pdf

### 输入文件示例
见test/input/
.
└── merge.qiime.xls         

### 运行环境及软件：
	北京238  R 4.2.3 (vegan,ggplot2,getopt)


### 资源消耗及运行时长
	输入文件物种数（行数）：8299
	rank：1CPU,3G,1min
	rarefaction：1CPU,10G,2min
	accumulation：1CPU,10G,2min

### 输出文件示例
.
├── allsample.accumulation.curve.pdf         物种累积曲线
├── allsample.rank.curve.pdf                 等级丰度曲线
└── allsample.rarefaction.curve.pdf          稀释性曲线

主要结果文件说明：
（1）allsample.accumulation.curve.pdf 
横坐标表示样本量；纵坐标表示抽样后物种数目。
利用物种与功能累积曲线可以作为对样本量是否充分的判断， 曲线急剧上升表明样本量不足，需要增加抽样量；反之，则表明抽样充分，可以进行数据分析。
（2）allsample.rank.curve.pdf 
横坐标为物种按丰度排序的序号，纵坐标为对应的物种的相对丰度，每条曲线对应一个样品。
主要用于同时解释样品所含物种的丰富度和均匀度，物种的丰富度由曲线在横轴上的长度来反映，曲线越宽，表示物种的组成越丰富；物种组成的均匀度由曲线的形状来反映，曲线越平坦，表示物种组成的均匀程度越高。
（3）allsample.rarefaction.curve.pdf
横坐标为随机抽取的测序条数，纵坐标为基于该测序条数得到的物种数量,每条曲线代表一个样品。
该图反映了持续抽样下新特征（新物种）出现的速率：在一定范围内，随着测序条数的加大，若曲线表现为急剧上升则表示群落中有大量物种被发现；当曲线趋于平缓，则表示此环境中的物种并不会随测序数量的增加而显著增多。稀释曲线可以作为对各样本测序量是否充分的判断,曲线急剧上升表明测序量不足，需要增加序列条数；反之，则表明样品序列充分，可以进行数据分析。
### 注意事项
稀释性曲线 如果样本数量过多，该图无法显示，需要手动调整

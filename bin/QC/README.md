mk_QC:

*模块功能：三代下机数据合并统计，包括插入片段长度分布图，准确率分布图，数据量，数据产出比例
*模块版本： V1
*邮箱： mengli@genome.cn

###使用示例：
	make -f mk_QC config= indir= outdir= sample= Merge PB_CCS_QC

###软件：
	smrtlink_11.0：
		路径：/annoroad/data1/software/install/smrtlink_11.0/bin/smrtcmds/bin/pbmm2
		版本：smrtlink V11.0
	convert：镜像
	perl: 镜像


###运行环境：
	北京的k8s集群

###输入参数：
	config: 配置文件，包括软件及相关参数，默认为$(bin)/config/config，可选
	indir：输入目录，hifi_reads.bam文件所在的路径；如果多个bam文件夹,请放在indir目录下。indir格式要求：indir/*/*hifi_reads.bam，比须
	outdir: 输出目录，必须
	sample: 样本名，必须
	Merge: 模块，功能是对三代下机数据按照样本名称合并
	PB_CCS_QC: 模块，功能是对三代下机数据统计，包括插入片段长度分布图，准确率分布图，数据量，数据产出比例
	Stat_qc: 模块，整合多样本的数据统计文件
### 资源消耗
	requests.cpu = 1
	requests.memory = 3G
	image = conda_perl_r:v0.5

### 运行时长
	单样本：30-40min

### 输入文件示例
见test/input/
└── A479
    └── P01DY20323610-1_r64054_20201205_020915_2_B02
        └─P01DY20323610-1_r64054_20201205_020915_2_B02.hifi_reads.bam
        └─P01DY20323610-1_r64054_20201205_020915_2_B02.hifi_reads.bam.pbi
        └─P01DY20323610-1_r64054_20201205_020915_2_B02.hifi_reads.bam.xml
    └── P01DY20323610-1_r64022_20201205_020915_2_B01
        └─P01DY20323610-1_r64022_20201205_020915_2_B01.hifi_reads.bam
        └─P01DY20323610-1_r64022_20201205_020915_2_B01.hifi_reads.bam.pbi
        └─P01DY20323610-1_r64022_20201205_020915_2_B01.hifi_reads.bam.xml

### 输出文件

├── Merge_bam
│   └── A479
         └── A479.hifi.bam  #单样本的合并后的bam文件
         └── A479.hifi.bam.pbi  
         └── A479.hifi.fasta.gz  #bam文件转成fasta格式



./QC
└── A479
    ├── A479_hifi_accuracy_hist.pdf #HiFi Reads整体的质量分布图
    ├── A479_hifi_accuracy_hist.png
    ├── A479_hifi_readlength_hist.pdf #HiFi Reads长度分布统计图
    ├── A479_hifi_readlength_hist.png
    ├── A479_hifireads_stat.xls #HiFi Reads统计文件
    ├── A479.hifi.xml
    ├── A479_readlength_qv_hist2d.hexbin.pdf #样本的HiFi Reads准确度和长度分布统计图
    ├── A479_readlength_qv_hist2d.hexbin.png
└── All_hifireads_stat.xls #多样本的HiFi reads 统计文件   


### 文件解释说明
#*hifireads_stat.xls：
（1）Sample：样本名称；
（2）HiFi Reads：HiFi Reads的数量；
（3）HiFi Yield (bp)： HiFi Reads的总碱基数目；
（4）HiFi Read Length (mean, bp)：HiFi Reads的平均长度；
（5）HiFi Read Quality (median)：全部HiFi Reads质量值中值；
（6）max_length：最长的HiFi Reads长度；
（7）N50：HiFi reads 的N50;
（8）GC content: HiFi reads 的GC含量。


#hifi_readlength_hist.p*：
样本的HiFi Reads长度分布统计图
上图横坐标为reads长度，纵坐标为reads数量，可以通过上图看到全部HiFi Reads整体的长度分布。

#hifi_accuracy_hist.p*：
样本的HiFi Reads整体的质量分布图
上图横坐标为质量值，纵坐标为reads数量，可以通过上图看到全部HiFi Reads整体的质量分布。

#readlengt_hist2d.hexbin.p*：
样本的HiFi Reads准确度和长度分布统计图
上图横坐标为reads长度，纵坐标为质量值，颜色由浅及深代表reads数量由少到多，可以通过上图看到全部HiFi Reads质量值和长度分布的集中范围。



### 输出文件示例
见test/

├── Merge_bam
│   └── A479
         └── A479.hifi.bam  #单样本的合并后的bam文件
         └── A479.hifi.bam.pbi  
         └── A479.hifi.fasta.gz  #bam文件转成fasta格式


./QC
└── A479
    ├── A479_hifi_accuracy_hist.pdf #HiFi Reads整体的质量分布图
    ├── A479_hifi_accuracy_hist.png
    ├── A479_hifi_readlength_hist.pdf #HiFi Reads长度分布统计图
    ├── A479_hifi_readlength_hist.png
    ├── A479_hifireads_stat.xls #HiFi Reads统计文件
    ├── A479.hifi.xml
    ├── A479_readlength_qv_hist2d.hexbin.pdf #样本的HiFi Reads准确度和长度分布统计图
    ├── A479_readlength_qv_hist2d.hexbin.png
└── All_hifireads_stat.xls #多样本的HiFi reads 统计文件   


### 注意事项
ags run *ini 投递




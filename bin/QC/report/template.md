@@@@QC
MainMenu:数据质控
SubMenu:数据统计和分布
P:#,;#PacBio测序的下机数据的保存格式为BAM，下机的Subreads使用PacBio官方软件SMRT Link中的ccs模块进行CCS分析得到HiFi reads，基于HiFi reads进行后续的分析。
P:#,;#数据量信息如下表：
Table:upload/*QC/All_hifireads_stat.xls,,8,850,,0,HiFi Reads统计表
PRE:,,;
（1）Sample：样本名称；
（2）HiFi Reads：下机HiFi Reads数目；
（3）HiFi Yield (bp)：HiFi Reads碱基总数；
（4）HiFi Read Length (mean, bp): HiFi Reads平均长度；
（5）HiFi Read Quality (median) ：HiFi Reads质量值中位数；
（6）Max Length：最长的HiFi Reads长度；
（7）N50：HiFi Reads的N50；
（8）GC content: HiFi Reads的GC含量。
PRE
P:#,;#HiFi Reads统计结果下载:
Excel:upload/*QC/All_hifireads_stat.xls,,,HiFi Reads统计结果下载：
P:#,;#绘制各个样本的HiFi Reads准确度分布统计图如下：
Image:upload/*_QC/*_hifi_accuracy_hist.png,400,4,HiFi Reads准确度分布图
P:#,;#横坐标为质量值，纵坐标为reads数量，可以通过上图看到全部HiFi Reads整体的质量分布。
P:#,;#HiFi Reads准确度分布图下载：
Excel:upload/*_QC/*_hifi_accuracy_hist.png,,,HiFi Reads准确度分布图下载：
P:#,;#绘制各个样本的HiFi Reads长度分布统计图如下：
Image:upload/*QC/*_hifi_readlength_hist.png,400,4,HiFi Reads长度分布图
P:#,;#横轴为HiFi reads长度，纵轴为HiFi reads数量，可以通过上图看到全部HiFi Reads整体的长度分布。
P:#,;#HiFi Reads长度分布图下载：
Excel:upload/*QC/*_hifi_readlength_hist.p*,,,HiFi Reads长度分布图下载：


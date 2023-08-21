'''
功能：按照给定的Bin范围将各个样本的read进行统计并绘制柱形图
输入文件：
PB_16s_arrange/cutadapter.read_stat.tsv  所有样本所有序列的长度文件
第一列：read ID
第二列：read 长度
第三列：GC含量
第四列：平均质量值
第四列：read所属样本的名称

输出文件：
按照样本将read划Bin输出并绘图

'''
#! /usr/bin/env python3
import argparse
import sys
import os
import re
import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



bindir = os.path.abspath(os.path.dirname(__file__))
filename=os.path.basename(__file__)

__author__='tu chengfang '
__mail__= 'chengfangtu@genome.cn'

# ====== 公共模块 =================================
class Log():
	def __init__( self, filename, funcname = '' ):
		self.filename = filename 
		self.funcname = funcname
	def format( self, level, message ) :
		date_now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
		formatter = ''
		if self.funcname == '' :
			formatter = '\n{0} - {1} - {2} - {3} \n'.format( date_now, self.filename, level, message )
		else :
			
			formatter = '\n{0} - {1} - {2} -  {3} - {4}\n'.format( date_now, self.filename, self.funcname, level, message )
		return formatter
	def info( self, message ):
		formatter = self.format( 'INFO', message )
		sys.stdout.write( formatter )
	def debug( self, message ) :
		formatter = self.format( 'DEBUG', message )
		sys.stdout.write( formatter )
	def warning( self, message ) :
		formatter = self.format( 'WARNING', message )
		sys.stdout.write( formatter )
	def error( self, message ) :
		formatter = self.format( 'ERROR', message )
		sys.stderr.write( formatter )
	def critical( self, message ) :
		formatter = self.format( 'CRITICAL', message )
		sys.stderr.write( formatter )

def get_sample_list( sample_file)	:
	sample_list = []
	with open( sample_file, 'r') as infile:
		for line in infile:
			if line.startswith('Sample'):continue
			tmp = line.rstrip().split('\t')
			sample = tmp[0]
			if sample not in sample_list :
				sample_list.append(sample)
	return sample_list

def get_bin( config ):
	bins=[]
	with open( config, 'r') as infile :
		for line in infile:
			tmp = line.rstrip()
			bins.append(int(tmp))
	return bins
			
def len_count_plot( read_count, bins, outdir, sample):
	#将read_count 转化为区间
	segment = pd.cut(read_count, bins,right=False)
	#统计每种长度区间的频数
	counts = pd.value_counts(segment,sort=False).values
	outfile = '{0}/{1}.pdf'.format( outdir, sample )
	statfile = open('{0}/{1}.xls'.format( outdir, sample ),'w')
	
	labels = [str(bins[i])+'-'+str(bins[i+1]) for i in range(len(bins)-1)]
	statfile.write('\t'.join(labels)+'\n')
	counts_str = [ str(i) for i in counts ]
	statfile.write('\t'.join(counts_str)+'\n')
	
	df = pd.DataFrame( counts, index=labels)
	plt.figure(figsize=(3,2))
	df.plot( kind='bar',legend=False,width=0.8,color='#004DA1',linewidth=0)
	plt.ylabel("Read Count")
	plt.xlabel("lenght(bp)")
	plt.subplots_adjust(bottom=0.2) #x-label显示不全，通过调整bottom进行了调整
	plt.gca().set_xticklabels(labels, rotation=45) #将横坐标倾斜45度
	plt.savefig(outfile)
	statfile.close()

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='stat of raw ccs',dest='input',required=True)
	parser.add_argument('-s','--sample',help='sample_list',dest='sample',required=True)
	parser.add_argument('-c','--config',help='config of len',dest='config',required=True)
	parser.add_argument('-o','--outdir',help='output file',dest='outdir',required=True)
	args=parser.parse_args()
	
	bins = get_bin(args.config)
	my_log.info("bin为:{0}".format(bins))
	sample_list = get_sample_list( args.sample )
	#my_log.info("样本为:{0}".format(sample_list))
	
	for sample in sample_list:
		my_log.info("正在处理 :{0}".format( sample ))
		read_count = []
		with open( args.input, 'r') as infile:
			for line in infile:
				if line.startswith('#') : continue
				if line.startswith('Sample') : continue
				tmp = line.rstrip().split('\t')
				len = tmp[1]
				sample_name = tmp[4]
				if sample_name != sample: continue
				read_count.append(len)
		#my_log.info("绘图处理 :{0}".format( sample ))
		len_count_plot( read_count, bins, args.outdir, sample)

if __name__ == '__main__':
	my_log = Log(filename)
	main()
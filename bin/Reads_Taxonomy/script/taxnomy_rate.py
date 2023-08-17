'''
统计每个样本注释上的reads的百分比

输入文件：
1）过滤后的统计文件，里面有Effective reads
2）物种注释后的ASV统计文件，里面有ASV对应的reads数量（即注释上的reads数量）

输出结果(转置)
样本  Effective reads  taxnomy_reads taxnomy_rate
'''


#! /usr/bin/env python3
import argparse
import sys
import os
import re
import datetime
import glob
import json
import configparser

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

def get_effective_read( infile ):
	'''
    获取有效reads数量
    输入：过滤后的统计文件，标题为 Sample  Raw Reads       Effective Reads Effective Rate(%)       Average len(bp)，第一列为样本名
    return:
    effctive_dic key:样本;value:effective reads(int)
    '''
	effective_dic = {}
	with open( infile, 'r') as input:
		for line in input:
			if line.startswith('Sample'):continue
			tmp = line.rstrip().split('\t')
			sample_name = tmp[0]
			effective_reads = int(tmp[2])
			if sample_name not in effective_dic:
				effective_dic[sample_name] = effective_reads
			else:
				my_log.error("样本名称重复：{0} 在{1} 中重复".format( sample_name, infile ))
	return effective_dic
			
def get_tax_read(infile):
	'''
    获取注释上的reads数量
    输入：Taxnomy注释后的统计文件
    第一行为样本名称，第一行第一列为Sample
    第二行第一列为：ASV Number
    第三行第一列为：Read Number（需要的值）
    return:
    anno_dic key:样本;value:Read Number(Int)
    '''
	anno_dic = {}
	sample_list = []
	with open( infile, 'r') as input:
		for line in input:
			tmp = line.rstrip().split('\t')
			if line.startswith('Sample'):
				sample_list = tmp[1:]
				for sample in sample_list:
					anno_dic[sample] = 0
				continue
			elif line.startswith('Read Number'):
				read_info = tmp[1:]
				for sample_index,sample_name in enumerate(sample_list):
					anno_dic[sample_name] += int(read_info[sample_index]		)
	return anno_dic,sample_list

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input of filter stat',dest='input',required=True)
	parser.add_argument('-s','--stat',help='stat of asv',dest='stat',required=True)
	parser.add_argument('-o','--output',help='output',dest='output',required=True)
	args=parser.parse_args()
	
	effective_dic = get_effective_read(args.input)
	anno_dic, sample_list = get_tax_read(args.stat)
	with open(args.output,'w') as outfile:
		head = ['Sample','Effective Read','Taxonomy Read','Rate(%)']
		outfile.write( '\t'.join( head)+'\n')
		for sample in sample_list:
			if sample not in effective_dic:
				my_log.error("{0} 不在 {1}中".format( sample,args.input))
				sys.exit(1)
			if sample not in anno_dic:
				my_log.error("{0} 不在 {1}中".format( sample,args.stat))
				sys.exit(1)
			effective_reads = effective_dic[sample]
			anno_reads = anno_dic[sample]
			anno_rate = '{0:.2f}'.format(100*anno_reads/effective_reads)
			out_value = [sample,str(effective_reads),str(anno_reads),anno_rate]
			outfile.write( '\t'.join( out_value)+'\n')
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
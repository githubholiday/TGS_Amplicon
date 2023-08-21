'''
根据原始ccs统计文件和长度文件等，计算过滤后的数据
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


def read_input( input ):
	'''
    获取各个样本的下机ccs数据
    '''
	sample_stat_dict = {}
	sample_list = []
	with open(input, 'r') as infile:
		for line in infile:
			tmp = line.rstrip().split('\t')
			if line.startswith("Sample"):
				for sample in tmp[1:]:
					if sample not in sample_stat_dict:
						sample_stat_dict[sample] = {}
					if sample not in sample_list :
						sample_list.append(sample)
			elif line.startswith("HiFi Reads"):
				for index,read in enumerate(tmp[1:]):
					sample_name = sample_list[index]
					sample_stat_dict[sample_name]['Raw Reads']=read.replace(',','')
	return sample_stat_dict
					

def read_len_stat( input,sample_stat_dict ):
	with open( input, 'r') as infile:   
		for line in infile:
			if line.startswith('sample'):continue
			tmp = line.rstrip().split('\t')
			sample_name = tmp[0]
			effective_reads = tmp[2]
			mean_length = tmp[3]
			if sample_name not in sample_stat_dict:
				my_log.error("输入文件样本不对应：-l 参数中的样本 {0} 不在 -i 参数文件中".format(sample_name))
				sys.exit(1)
			Raw_Reads = int(sample_stat_dict[sample_name]['Raw Reads'])
			sample_stat_dict[sample_name]['Effective Reads'] = effective_reads
			sample_stat_dict[sample_name]['Average len(bp)'] = mean_length
			sample_stat_dict[sample_name]['Effective Rate(%)'] = '{0:.2f}'.format(100*int(effective_reads)/Raw_Reads)
	return sample_stat_dict
			
			
def write_file( output, sample_stat_dic):
	with open(output, 'w') as outfile :
		head = ['Sample','Raw Reads','Effective Reads','Effective Rate(%)','Average len(bp)']
		outfile.write("\t".join(head)+'\n')
		for sample in sample_stat_dic:
			Raw_Reads = int(sample_stat_dic[sample]['Raw Reads'])
			if 'Effective Reads' not in sample_stat_dic[sample]:
				my_log.info("输入文件样本不对应：-i 参数中的样本 {0} 不在 -l 参数文件中".format( sample))
				sys.exit(1)
			effective_reads = sample_stat_dic[sample]['Effective Reads'] 
			mean_length = sample_stat_dic[sample]['Average len(bp)']
			effective_rate =sample_stat_dic[sample]['Effective Rate(%)']
			out = [ sample, str(Raw_Reads), effective_reads, effective_rate, mean_length]
			outfile.write("\t".join(out)+'\n')

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='stat of raw ccs',dest='input',required=True)
	parser.add_argument('-l','--lenf',help='length stat of effective',dest='lenf',required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',required=True)
	args=parser.parse_args()
	sample_stat_dict = read_input(args.input)#读取原始数据产出
	sample_stat_dict = read_len_stat( args.lenf,sample_stat_dict ) 
	write_file( args.output, sample_stat_dict)
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()

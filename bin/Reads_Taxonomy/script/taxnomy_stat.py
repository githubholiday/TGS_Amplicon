'''
输入文件：
taxnomy的物种注释文件
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

def col_add( sample_info, sample_read_list ):
	'''
    将每列的reads数进行相加
    sample_info：list,每个元素是每列的值
    sample_read_list：list,原每列的加和值
    '''
	sample_read_list_new = [i+j for i,j in zip(sample_read_list, sample_info )]
	return sample_read_list_new

def count_tax_type(sample_info, tax_num_list):
	'''
    将每列大于0的赋值为1，其余为0,其实就是为了计数ASV数量
    '''
	tax_num_new = []
	for i in sample_info:
		if i > 0: tax_num_new.append(1)
		else:tax_num_new.append(0)
	tax_num_list_new = [i+j for i,j in zip( tax_num_list, tax_num_new)]
	return tax_num_list_new
			
def get_effective_read( stat_file) :
	'''
    根据过滤统计文件获取 
    '''
def get_sample_taxnomy_stat( taxnomy, taxnomy_dic, sample_list, sample_info):
	'''
	将每个样本的不同物种注释上的reads数进行相加
	paramters:
		taxnomy:物种信息，一般为d__Bacteria;p__Proteobacteria;c__Alphaproteobacteria;o__Rhodobacterales;****
		taxnomy_dic:样本的物种注释reads字典。key:taxnomy value={sample:num}
		sample_list:样本列表
		sample_info:样本对应的物种注释reads数量
	return : taxnomy_dic
	'''
	if taxnomy not in taxnomy_dic:
		taxnomy_dic[taxnomy] = {}
	for sample_index, sample in enumerate(sample_list ):
		if sample not in taxnomy_dic[taxnomy] :
			taxnomy_dic[taxnomy][sample] = 0 
		sample_tax_num = sample_info[ sample_index]
		taxnomy_dic[taxnomy][sample] += sample_tax_num
	return taxnomy_dic


def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input of taxnomy',dest='input',required=True)
	#parser.add_argument('-s','--stat',help='stat of effective read',dest='stat',required=True)
	parser.add_argument('-o','--output',help='output',dest='output',required=True)
	parser.add_argument('-to','--taxnomy_out',help='taxnomy_out',dest='taxnomy_out',required=True)
	args=parser.parse_args()
	

	sample_list = []
	taxonomy_dic = {}
	sample_read = []
	with open( args.input, 'r') as infile:
		for line in infile:
			if line.startswith('#') : continue
			tmp = line.rstrip().split('\t')
			if line.startswith('id'):
				sample_list = tmp[4:]
				sample_num = len(sample_list)
				sample_read_list = [0]*sample_num
				tax_num_list = [0]*sample_num
				continue
			taxonomy = tmp[2]
			sample_info = [int(i) for i in tmp[4:]]
			#将每列的值进行相加，获取每个样本注释上的reads数量
			sample_read_list = col_add(sample_info, sample_read_list)
			taxonomy_dic =get_sample_taxnomy_stat(taxonomy,taxonomy_dic,sample_list, sample_info)
            #将每列大于0的个数累积，为ASV数量
			tax_num_list = count_tax_type(sample_info, tax_num_list)
			
	with open( args.output, 'w') as outfile :
		head = ['Sample']+sample_list
		outfile.write("\t".join(head)+'\n')
			
		tax_num_list_str = [str(i) for i in tax_num_list]
		ASV_num = ['ASV Number']+tax_num_list_str
		outfile.write("\t".join(ASV_num)+'\n')

		sample_read_list_str =  [str(i) for i in sample_read_list]	
		read_num =  ['Read Number']+sample_read_list_str
		outfile.write("\t".join(read_num)+'\n')  
	my_log.info("输出文件为: {0}".format(args.output)) 
	
	with open( args.taxnomy_out, 'w') as out:
		head = ['Taxnomy']+sample_list
		out.write('\t'.join(head)+'\n')
		for tax in taxonomy_dic:
			tax_list = [tax]
			for sample in sample_list:
				num = str(taxonomy_dic[tax][sample])
				tax_list.append(num)
			out.write('\t'.join(tax_list)+'\n')
	my_log.info("输出文件为: {0}".format(args.taxnomy_out)) 
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
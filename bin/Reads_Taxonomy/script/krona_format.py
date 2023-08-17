'''


输入文件：


输出文件：
按照样本输出各样本的不同层级的物种数量

构思：
1）Open文件只需要第三列和5列之后的信息
2）第二行信息不需要
3）


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

def deal_taxnomy( tax_dic, tax_str, sample_info ):
	sample_num = len(sample_info)
	tax_list = tax_str.split(';')
	kingdom = tax_list[0]
	division = '|'.join(tax_list[0:2])
	class_name = '|'.join(tax_list[0:3])
	order = '|'.join(tax_list[0:4])
	family = '|'.join(tax_list[0:5])
	genus = '|'.join(tax_list[0:6])
	species = '|'.join(tax_list[0:7]) #tax_str
	new_tax_list = [kingdom,division, class_name, order,family,genus,species  ]
	for tax in new_tax_list :
		if tax not in tax_dic:
			tax_dic[tax] = [0]*sample_num
		tax_sample_num_list = tax_dic[tax]
		tax_sample_info  = [i+j for i,j in zip(tax_sample_num_list,sample_info )]
		tax_dic[tax] = tax_sample_info
	return tax_dic

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input of taxnomy',dest='input',required=True)
	parser.add_argument('-o','--output',help='outdir,default=indir',dest='output',required=True)
	args=parser.parse_args()
	

	sample_list = []
	taxnomy_dic = {}
	with open( args.input, 'r') as infile, open(args.output, 'w') as outfile:
		for line in infile:
			if line.startswith('#') : continue
			tmp = line.rstrip().split('\t')
			taxnomy= tmp[0]
			num = tmp[1]
			taxnomy_list = '\t'.join(taxnomy.split('|'))
			out_value = [num,taxnomy_list]
			outfile.write('\t'.join(out_value)+'\n')
			
	
				
                    
                
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
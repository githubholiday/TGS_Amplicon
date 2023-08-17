'''
将所有样本的所有物种信息合并的文件，按照指定的等级进行拆分
等级划分为：
{'kingdom':'k__','division':'d__','class':'c__','order':'o__' ,'family':'f__','genus':'g__','species':'s__'}

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
os.environ['OPENBLAS_NUM_THREADS'] = '1'
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

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input of taxnomy',dest='input',required=True)
	parser.add_argument('-o','--output',help='output',dest='output',required=True)
	parser.add_argument('-t','--type',help='type of class',dest='type',default='species')
	args=parser.parse_args()
	
	relation_dict = {'domain':'d__','division':'p__','class':'c__','order':'o__' ,'family':'f__','genus':'g__','species':'s__'}
	if args.type not in relation_dict:
		my_log.error("参数提供错误 -t:可选项为kingdom,division,class,order,family,genus,species ")
		sys.exit(1)
	else:
		required_type = relation_dict[args.type]
	with open(args.input, 'r') as infile, open(args.output, 'w') as outfile :
		for line in infile:
			if line.startswith('Sample'): 
				outfile.write(line)		
				continue
			tmp = line.rstrip().split('\t')
			tax = tmp[0]
			my_tax = tax.split('|')[-1]
			if my_tax.startswith(required_type) :
				#tmp[0] = my_tax
				outfile.write('\t'.join(tmp)+'\n')			
				
		
	
if __name__ == '__main__':
	my_log = Log(filename)
	main()

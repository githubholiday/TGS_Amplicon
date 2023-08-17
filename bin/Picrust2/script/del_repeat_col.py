'''
删除重复列名，只保留第一个，所以默认输入文件第一行为表头
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

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--infile',help='infile',dest='infile',required=True)
	parser.add_argument('-r','--rm',help='the column name which you want to delete',dest='rm',required=True)
	parser.add_argument('-o','--outfile',help='outfile',dest='outfile',required=True)
	args=parser.parse_args()
	
	remain_index_list = []
	flag = 0
	with open( args.infile, 'r') as input,open(args.outfile,'w') as output:
		for line_index, line in enumerate( input):
			tmp = line.rstrip().split('\t')
			if line_index == 0 :
				for col_index,col_name in enumerate(tmp):
					if col_name == args.rm and flag == 0  :
						remain_index_list.append(col_index)
						flag += 1
					elif col_name != args.rm:
						remain_index_list.append(col_index)
			tt = [ tmp[i] for i in remain_index_list]
			output.write('\t'.join( tt )+'\n')
			
			
                
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
'''
将输入文件按列进行格式化（z-score)
'''


#! /usr/bin/env python3
import argparse
import sys
import os
import re
import datetime
import pandas as pd
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
	args=parser.parse_args()
	df = pd.read_table( args.input, sep='\t',index_col=0) #将第一列作为index
	head = df.columns
	dfs = []
	for sample in head:
		dd = df[sample]
		data = (dd-dd.mean())/dd.std()
		dfs.append(pd.DataFrame(data))
	out_data = pd.concat(dfs,axis=1)
	out_data.to_csv( args.output, sep='\t',index=True)
	
if __name__ == '__main__':
	my_log = Log(filename)
	main()

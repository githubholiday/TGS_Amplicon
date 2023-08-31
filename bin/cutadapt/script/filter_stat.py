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

def read_len_stat( input, output ):
	head = ['Sample','Raw Reads','Effective Reads','Effective Rate(%)','Average len(bp)']
	with open( input, 'r') as infile, open( output,'w') as outfile:   
		outfile.write("\t".join(head)+'\n')
		for line in infile:
			if line.startswith('sample'):continue
			tmp = line.rstrip().split('\t')
			sample_name = tmp[0]
			Raw_Reads = tmp[1]
			effective_reads = tmp[2]
			mean_length = tmp[3]
			effective_rate = '{0:.2f}'.format(100*int(effective_reads)/int(Raw_Reads))
			out = [ sample_name, str(Raw_Reads), effective_reads, effective_rate, mean_length]
			outfile.write("\t".join(out)+'\n')
			

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-l','--lenf',help='length stat of effective',dest='lenf',required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',required=True)
	args=parser.parse_args()

	sample_stat_dict = read_len_stat( args.lenf, args.output)
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()

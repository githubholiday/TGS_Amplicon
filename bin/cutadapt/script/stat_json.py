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
		
def parse_json(infile):
	input = open(infile,'r')
	json_decode = json.load(input)
	return json_decode

def get_stat(json_decode):
	inread = json_decode['read_counts']['input']
	outread = json_decode['read_counts']['output'] 
	return inread, outread
    
def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--infile',help='cutadapt json file list',dest='infile',required=True)
	parser.add_argument('-s','--sample',help='sample name',dest='sample',required=True)
	parser.add_argument('-o','--outfile',help='outfile',dest='outfile',required=True)
	args=parser.parse_args()

	json_decode = parse_json(args.infile)
	inread, outread = get_stat(json_decode)
	with open( args.outfile, 'w') as output:
		output.write('sample\tinput_reads\tdemuxed_reads\n')
		output.write('{0}\t{1}\t{2}\n'.format(args.sample, inread, outread))


if __name__ == '__main__':
	my_log = Log(filename)
	main()
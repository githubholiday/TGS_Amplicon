'''
绘制OTU数量Barplot图
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

def read_input( infile ):
	sample_list = []
	asv_num_list = []
	with open(infile, 'r') as input:
		for line in input:
			tmp = line.rstrip().split('\t')
			if line.startswith( 'Sample'):
				for i in tmp[1:]:
					if i not in sample_list : sample_list.append(i)
					else : sys.exit(1)
			if line.startswith( 'ASV Number'):
				for i in tmp[1:]:
					asv_num_list.append(int(i))
	return sample_list, asv_num_list
		
def plot_bar( sample_list, asv_num_list, outfile):
	data = pd.DataFrame( asv_num_list, index=sample_list)

	plt.figure(figsize=(10,10))
	data.plot( kind='bar',legend=False,width=0.3,color='#004DA1',linewidth=0)
	plt.ylabel("Feature Count")
	plt.xlabel("Sample")
	plt.subplots_adjust(bottom=0.4) #x-label显示不全，通过调整bottom进行了调整
	plt.gca().set_xticklabels(sample_list, rotation=45) #将横坐标倾斜45度
	plt.savefig(outfile)
	my_log.info("输出文件:{0}".format( outfile))

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='stat of raw ccs',dest='input',required=True)
	parser.add_argument('-o','--outfile',help='output file',dest='outfile',required=True)
	args=parser.parse_args()
	
	sample_list, asv_num_list  = read_input( args.input )
	
	plot_bar(sample_list, asv_num_list, args.outfile)
	

if __name__ == '__main__':
	my_log = Log(filename)
	main()
'''
使用单样本的物种文件计算每个比较组中的物种分布情况
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

def get_group_info(group_file):
	group_dic= {}
	with open(group_file, 'r') as infile:
		for line in infile:
			tmp = line.rstrip().split('\t')
			group_name = tmp[0]
			sample_list = tmp[1:]
			if group_name not in group_dic:
				group_dic[group_name] = sample_list
			else:
				my_log.error("group内容重复了:{0}".format( group_name ))
	return group_dic

def get_group_count( sample_file, group_dic ):
	with open( sample_file, 'r') as infile:
		for line in infile:
			if line.startswith( 'Sample') : continue
			tmp = line.rstrip().split('\t')
			species = tmp[0]
			num = int(tmp[1])
			if species not in group_dic:
				group_dic[species] = 0 
			group_dic[species] += num		
	return group_dic
		    
def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--indir',help='indir of sample format file',dest='indir',required=True)
	parser.add_argument('-g','--group',help='group file',dest='group',required=True)
	parser.add_argument('-o','--outdir',help='outdir,default=indir',dest='outdir',required=True)
	args=parser.parse_args()
	
	group_dic = get_group_info(args.group)
	
	for group in group_dic:
		group_count_dic = {}
		sample_list = group_dic[group]
		for sample in sample_list :
			sample_file = '{0}/{1}.format.xls'.format( args.indir, sample)
			group_count_dic = get_group_count( sample_file, group_count_dic )
		group_file = '{0}/{1}.format.xls'.format( args.outdir, group)
		with open(group_file,'w') as outfile:
			for species in group_count_dic:
				count = str(group_count_dic[species])
				out_value = [ species, count]
				outfile.write('\t'.join(out_value)+'\n')
    
    
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()

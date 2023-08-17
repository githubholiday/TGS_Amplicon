'''

功能：COG的注释总文件进行拆分，拆分成按照样本和比较组的，如果值为0的为没注释上
输入：
1）COG的注释总文件:picrust2的输出文件,并在最后一列增加了Class注释列
2）COG数据库cog.txt:每个COG编号对应的大类名称
输出：
1）样本输出：

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
		
def read_whog( infile ) :
	'''
    通过COG的whog.txt文件获取COG编号和大分类的关系
    cog_dict：字典
        key:str,cog编号
        value:str,大分类，如[A]
    '''
	cog_dict = {}
	with open(infile, 'r') as input:
		for line in input:
			if not line.startswith( "[") : continue
			tmp = line.rstrip().split(' ')
			class_id = tmp[0]
			cog_id = tmp[1]
			if cog_id not in cog_dict:
				cog_dict[cog_id] = class_id
	return cog_dict

def read_fun(infile):
	class_dict = {}
	with open(infile,'r') as input:
		for line in input:
			if not line.startswith( "[") : continue
			tmp = line.strip().split(' ')
			class_id = tmp[0]
			class_name = ''.join(tmp[1:])
			if class_id not in class_dict:
				class_dict[class_id] = class_name
	return class_dict

def init_dict( sample_list,sample_cog_dic):
	'''
	初始化字典
	'''
	for sample in sample_list:
		if 	sample not in sample_cog_dic:
			sample_cog_dic[sample] = {}
	return sample_cog_dic

def add_dict( sample_list, sample_num_list, sample_cog_dict, class_name ):
	'''
    判断样本是否注释到COG上，如果注释上，则+1
    '''
	for index,sample_num in enumerate(sample_num_list):
		sample_rich = float( sample_num )
		if sample_rich == '0.0' : continue
		sample_name = sample_list[index]
		if class_name not in sample_cog_dict[sample_name]:
			sample_cog_dict[sample_name][class_name] = 0 
		sample_cog_dict[sample_name][class_name] += 1
	return sample_cog_dict
		
		

def get_annotations( infile ):
	'''
    计算每个样本注释上的条目的数量
    '''
	sample_cog_dic = {}
	my_log.info("正在处理：{0}".format(infile))
	with open( infile, 'r') as input:
		for line in input:
			tmp = line.rstrip().split('\t')
			cog_id = tmp[0]
			class_name = tmp[-1]
			if line.startswith( "function") :
				sample_list = tmp[1:-1]#去掉第一个和最后一个，中间都是样本名称
				sample_cog_dic = init_dict( sample_list, sample_cog_dic )
			else:
				sample_num_list = tmp[1:-1] 
				sample_cog_dict = add_dict( sample_list, sample_num_list, sample_cog_dic, class_name )
	return sample_cog_dict
				

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-a','--anno',help='anno file',dest='anno',required=True)
	parser.add_argument('-o','--outdir',help='outdir',dest='outdir',required=True)
	args=parser.parse_args()
	sample_anno_dict = get_annotations( args.anno )
	my_log.info("正在按样本输出：{0}".format( args.outdir))
	for sample in sample_anno_dict:
		outfile = '{0}/{1}.cog.stat.xls'
		cog_info = sample_anno_dict[sample]
		with open(outfile,'w') as outfile:
			head = ['function code','function', 'number']
			outfile.write('\t'.join(head)+'\n')
			for cog_name in cog_info :
				cog_num = cog_info[cog_name]
				tmp = cog_name.split(']')
				function_code = tmp[0].replace('[]','')
				function = tmp[1]
				value = [ function_code, function, str(cog_num)]
				outfile.write('\t'.join(value)+'\n')
				
				
				
			
			

	
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
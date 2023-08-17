'''

功能：COG的注释总文件进行拆分，拆分成按照样本和比较组的，如果值为0的为没注释上
输入：
1）COG的注释总文件:picrust2的输出文件,并在最后一列增加了Class注释列
2）COG数据库cog.txt:每个COG编号对应的大类名称
输出：
1）样本输出-示例
function code   function        number
A       RNA processing and modification 2


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
		
def read_fun( funfile):
	fun_dict = {}
	with open( funfile, 'r') as infile:
		for line in infile:
			tmp = line.rstrip().split('\t')
			class_id = tmp[0]
			class_name = tmp[1]
			fun_dict[class_id] = class_name
	return fun_dict

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
		if sample_rich == '0.0' : 
			continue #如果值为0，说明没注释上，直接跳过
		sample_name = sample_list[index] #根据列的Index获取对应的样本名称
		if class_name not in sample_cog_dict[sample_name]:
			sample_cog_dict[sample_name][class_name] = 0 
		sample_cog_dict[sample_name][class_name] += 1
	return sample_cog_dict
		
		

def get_annotations( infile ):
	'''
    计算每个样本注释上的条目的数量
    '''
	sample_cog_dic = {}
	sample_list = []
	with open( infile, 'r') as input:
		for line in input:
			tmp = line.rstrip().split('\t')
			cog_id = tmp[0]
			class_id = tmp[-2]
			if line.startswith( "function") :
				sample_list = tmp[1:-2] #去掉第一个和最后一个，中间都是样本名称
				sample_cog_dic = init_dict( sample_list, sample_cog_dic )
			else:
				sample_num_list = tmp[1:-2] 
				sample_cog_dict = add_dict( sample_list, sample_num_list, sample_cog_dic, class_id )
	return sample_cog_dict
				

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-a','--anno',help='anno file',dest='anno',required=True)
	parser.add_argument('-f','--fun',help='fun file',dest='fun',required=True)
	parser.add_argument('-o','--outdir',help='outdir',dest='outdir',required=True)
	args=parser.parse_args()
	
	my_log.info("正在处理：{0}".format(args.anno))
	sample_anno_dict = get_annotations( args.anno )

	my_log.info("正在处理：{0}".format(args.fun))
	fun_dict = read_fun( args.fun )
	#print(fun_dict)
	my_log.info("正在按样本输出：{0}/*.cog.stat.xls".format( args.outdir))
	for sample in sample_anno_dict:
		#按照样本定义输出文件
		outfile = '{0}/{1}.cog.stat.xls'.format( args.outdir, sample)
		#cog_info[class_id] = 5
		cog_info = sample_anno_dict[sample]
		with open(outfile,'w') as outfile:
			head = ['function code','function', sample]
			outfile.write('\t'.join(head)+'\n')
			#print(cog_info)
            
			for class_id in sorted(fun_dict.keys()) :
				class_name = fun_dict[class_id]
				if class_id in cog_info:
					cog_num = cog_info[class_id]
				else:
					cog_num = 0
				value = [ class_id, class_name, str(cog_num)]
				outfile.write('\t'.join(value)+'\n')
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
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
		
def read_map( mapfile):
	map_dict = {}
	classI_II_dict = {}
	with open( mapfile, 'r') as infile:
		for line in infile:
			tmp = line.rstrip().split('\t')
			if line.startswith( 'Map'): continue
			map_id = tmp[0]
			classIII = tmp[1]
			classII = tmp[2]
			classI = tmp[3]
			if map_id in  map_dict:
				my_log.warning("map id重复:{0}".format( mapfile ))
				continue
			map_dict[map_id] = [classIII, classII, classI]
			if classII not in classI_II_dict:
				classI_II_dict[classII] = classI
	return map_dict, classI_II_dict

def init_dict( sample_list,sample_cog_dic):
	'''
	初始化字典
	'''
	for sample in sample_list:
		if 	sample not in sample_cog_dic:
			sample_cog_dic[sample] = {}
	return sample_cog_dic

def add_dict( sample_list, sample_num_list, sample_ko_dict, map_list ):
	'''
    判断样本是否注释到COG上，如果注释上，则+1
    '''
	for index,sample_num in enumerate(sample_num_list):
		sample_rich = float( sample_num )
		if sample_rich == '0.0' : 
			continue #如果值为0，说明没注释上，直接跳过
		sample_name = sample_list[index] #根据列的Index获取对应的样本名称
		for map_id in map_list:
			if map_id not in sample_ko_dict[sample_name]:
				sample_ko_dict[sample_name][map_id] = 0 
			sample_ko_dict[sample_name][map_id] += 1
	return sample_ko_dict
		
def get_annotations( infile ):
	'''
    计算每个样本注释上的条目的数量
    '''
	sample_ko_dic = {}
	sample_list = []
	with open( infile, 'r') as input:
		for line in input:
			tmp = line.rstrip().split('\t')
			ko_id = tmp[0]
			map_id_list = tmp[-1].split('|')
			if line.startswith( "function") :
				sample_list = tmp[1:-1] #去掉第一个和最后一个，中间都是样本名称
				sample_ko_dic = init_dict( sample_list, sample_ko_dic )
			else:
				sample_num_list = tmp[1:-1] 
				sample_ko_dic = add_dict( sample_list, sample_num_list, sample_ko_dic, map_id_list )
	return sample_ko_dic

def get_class_dict( class_name_list, ko_num, classII_dict, classI_dict  ):
	'''
    获取classII 和classI分类上注释到的数量
    '''
	classIII, classII, classI = class_name_list[0], class_name_list[1], class_name_list[2]
	if classII not in classII_dict :
		classII_dict[classII] = 0
	classII_dict[classII] += ko_num
	if classI not in classI_dict :
		classI_dict[classI] = 0
	classI_dict[classI] += ko_num
	return classII_dict,classI_dict

def write_classII( classII_dict, classI_II_dict, sample, outfile):
	head = ['ClassII','ClassI', sample]
	with open( outfile, 'w') as output:
		output.write('\t'.join(head)+'\n')
		for classII in classII_dict:
			anno_num = classII_dict[classII] #注释到classII上的数量
			classI = classI_II_dict[classII] #classII对应的classI的信息
			out_line = [ classII, classI, str(anno_num)]
			output.write('\t'.join(out_line)+'\n')

def write_classI( classI_dict, sample, outfile):
	head = ['ClassI', sample]
	with open( outfile, 'w') as output:
		output.write('\t'.join(head)+'\n')
		for classI in classI_dict:
			anno_num = classI_dict[classI] #注释到classI上的数量
			out_line = [ classI, str(anno_num)]
			output.write('\t'.join(out_line)+'\n')		
			

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-a','--anno',help='anno file',dest='anno',required=True)
	parser.add_argument('-m','--map',help='map pathway file',dest='map',required=True)
	parser.add_argument('-o','--outdir',help='outdir',dest='outdir',required=True)
	args=parser.parse_args()
	
	my_log.info("正在处理: {0}".format(args.anno))
	sample_anno_dict = get_annotations( args.anno )

	my_log.info("正在处理: {0}".format(args.map))
	map_dict, classI_II_dict = read_map( args.map ) #map_dict[map_id] = [classIII, classII, classI]

	classII_dict = {}
	classI_dict = {}

	my_log.info("正在按样本输出三级分类信息: {0}".format( args.outdir))
	for sample in sample_anno_dict:
		#按照样本定义输出文件
		outfile3 = '{0}/{1}.classIII.stat.xls'.format( args.outdir, sample)
		outfile2 = '{0}/{1}.classII.stat.xls'.format( args.outdir, sample)
		outfile1 = '{0}/{1}.classI.stat.xls'.format( args.outdir, sample)
		#ko_info[class_id] = 5
		ko_info = sample_anno_dict[sample] #每个样本的map对应关系字典
		with open(outfile3,'w') as output:
			head = ['Map','ClassIII', 'ClassII','ClassI',sample]
			output.write('\t'.join(head)+'\n')
			for map_id in sorted(map_dict.keys()) :
				class_name_list = map_dict[map_id]
				
				if map_id in ko_info:
					ko_num = ko_info[map_id]
				else:
					ko_num = 0
				value = [ map_id ]+ class_name_list+[ str(ko_num)]
				output.write('\t'.join(value)+'\n')
				classII_dict, classI_dict = get_class_dict(class_name_list, ko_num, classII_dict, classI_dict)
		write_classI( classI_dict, sample, outfile1)
		write_classII( classII_dict, classI_II_dict, sample, outfile2)
		
if __name__ == '__main__':
	my_log = Log(filename)
	main()
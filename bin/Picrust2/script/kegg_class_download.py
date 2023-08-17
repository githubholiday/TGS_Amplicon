'''

解析Kegg pathway页面信息，获取KEGG的层级关系
输入：
html文件
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
		
		
class Parse_Html():
	def __init__(self, html_file, outfile ):
		self.html = html_file
		self.outfile = outfile
	def html_main(self):
		class1_name = ''
		class2_name = ''
		class_dict = {}
		head = ['Map','Pathway',"ClassII",'ClassI']
		with open(self.html, 'r') as f, open(self.outfile, 'w') as output:
			output.write("\t".join(head)+'\n')
			for line in f:
				if line.startswith('<h4 id'):
					class1_name = self.get_class1( line )
					if class1_name not in class_dict:
						class_dict[class1_name] = {}
					continue
				if line.startswith('<b id'):
					class2_name = self.get_class2( line )
					if class2_name not in class_dict[class1_name]:
						class_dict[class1_name][class2_name] = []
					continue
				if line.startswith('    <dt>') and '<a href=' in line:
					map,pathway = self.get_map( line )
					value = [ 'map'+map, pathway, class2_name, class1_name]
					output.write('\t'.join(value)+'\n')
				
	def get_class1( self, line):
		tmp = line.rstrip().split(' ')
		meta = tmp[2].split('<')[0]
		return meta
	
	def get_class2( self, line):
		tmp = line.rstrip().split('>')
		meta_tmp = tmp[1].split('<')[0]
		meta = ' '.join(meta_tmp.split(' ')[1:])
		return meta
	
	def get_map( self, line):
		if 'small' in line :
			#'<dt>01100 <span class="small">M</span></dt><dd><a href="/pathway/map01100">Metabolic pathways</a></dd>'
            #['<dt', '01100 <span class="small"', 'M</span', '</dt', '<dd', '<a href="/pathway/map01100"', 'Metabolic pathways</a', '</dd', '']
			tmp = line.strip().split('>')
			map  = tmp[1].split(' ')[0]
			pathway = tmp[6].split('<')[0]
		else:
			#'<dt>00196</dt><dd><a href="/pathway/map00196">Photosynthesis - antenna proteins</a></dd>'
            #['<dt', '00196</dt', '<dd', '<a href="/pathway/map00196"', 'Photosynthesis - antenna proteins</a', '</dd', '']
			tmp = line.strip().split('>')
			map = tmp[1].split('<')[0]
			pathway = tmp[4].split('<')[0]
		return map, pathway
	
		
		
	

				

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-ht','--html',help='anno file',dest='html',required=True)
	parser.add_argument('-o','--outfile',help='outdir',dest='outfile',required=True)
	args=parser.parse_args()
	
	html_handle = Parse_Html( args.html, args.outfile)
	html_handle.html_main()
		 
if __name__ == '__main__':
	my_log = Log(filename)
	main()
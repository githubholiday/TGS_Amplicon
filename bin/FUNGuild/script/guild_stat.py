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

def get_column_index( tmp_list ):
	index_dict = {}
	for index, item in enumerate( tmp_list ):
		index_dict[item] = index
	return index_dict	

def get_confidence(confidence_value):
	confidence_list = []
	if confidence_value == 'all':
		confidence_list = ['Possible','Probable','Highly Probable']
	elif confidence_value == 'Possible':
		confidence_list = ['Highly Probable','Probable','Possible']
	elif confidence_value == 'Probable':
		confidence_list = ['Probable','Highly Probable']
	elif confidence_value == 'Highly Probable':
		confidence_list = ['Highly Probable']
	else:
		my_log.error("confidence参数错误，只能为 Possible,Probable,Highly Probable,all")
		sys.exit(1)
	return confidence_list

def fn_guild_dict():
	'''
    guild信息来源于https://github.com/UMNFuN/FUNGuild/blob/master/README.md
    Pathotroph:病例营养型
    Saprotroph:共生营养型
    Symbiotroph:腐生营养型
    '''
	guild_dict = {"Animal Pathogens":["Pathotroph",0],
			"Bryophyte Parasite":["Pathotroph",0],
			"Fungal Parasite":["Pathotroph",0],
			"Lichen Parasite":["Pathotroph",0],
			"Plant Pathogen":["Pathotroph",0],
			"Dung Saprotroph":["Saprotroph",0],
			"Leaf Saprotroph":["Saprotroph",0],
			"Plant Saprotroph":["Saprotroph",0],
			"Soil Saprotroph":["Saprotroph",0],
			"Undefined Saprotroph":["Saprotroph",0],
			"Wood Saprotroph":["Saprotroph",0],
			"Ectomycorrhizal":["Symbiotroph",0],
			"Ericoid Mycorrhizal":["Symbiotroph",0],
			"Endophyte":["Symbiotroph",0],
			"Endophyte":["Symbiotroph",0],
			"Lichenized":["Symbiotroph",0],
			"Others":["Others",0]
    }
	return guild_dict

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-g','--gulid_file',help='guild file',dest='gulid_file',required=True)
	parser.add_argument('-o','--output',help='output',dest='output',required=True)
	parser.add_argument('-c','--confidence',help='confidence of the result',dest='confidence',default='Highly Probable',choices=['Possible','Probable','Highly Probable','all'])
	args=parser.parse_args()
	
	confidence_list = get_confidence(args.confidence)
	guild_dict = fn_guild_dict()
	with open( args.gulid_file, 'r') as infile, open( args.output, 'w') as outfile:
		for line in infile:
			tmp = line.rstrip().split('\t')
			if line.startswith("OTU"):
				index_dict =  get_column_index(tmp)
				continue
			guild_name = tmp[index_dict['guild']]
			confidence = tmp[index_dict['confidenceRanking']]
			if confidence not in confidence_list: continue
			guild_name_list = guild_name.split('-')
			for guild_name_i in guild_name_list:
				if guild_name_i not in guild_dict :
					guild_dict["Others"][1] +=1
					continue
				guild_dict[guild_name_i][1] += 1
		outfile.write("guild\tcount\n")
		for guild_name in guild_dict:
			guild_type, guild_count = guild_dict[guild_name]
			outfile.write("{0}\t{1}\t{2}\n".format(guild_type,guild_name,guild_count))
			
    
				
			
        
	
	
if __name__ == '__main__':
	my_log = Log(filename)
	main()
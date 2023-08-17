'''
功能：统计pathway数量，并将其一一输出
输入：
1）map和pathway的统计文件
Map	ClassIII	ClassII	ClassI	Number
map00010	Glycolysis / Gluconeogenesis	Carbohydrate metabolism	Metabolism	62

输出：
1）outdir/prefix.classI.xls:等级1的统计结果
1）outdir/prefix.classII.xls:等级2的统计结果
1）outdir/prefix.classIII.xls:等级3的统计结果
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


def read_infile( infile ):
	'''
    计算每个样本注释上的条目的数量
    '''
	classI_dict = {}
	classII_dict = {}
	classIII_dict = {}
	classI_II_dict = {} #classI和classII的对应关系
	with open( infile, 'r') as input:
		for line in input:
			if line.startswith('Map'):continue
			tmp = line.rstrip().split('\t')
			classIII = tmp[1]
			classII = tmp[2]
			classI = tmp[3]
			number = int(tmp[4])
			classI_dict =  init_dict(classI, number, classI_dict )
			classII_dict =  init_dict(classII, number, classII_dict )
			classIII_dict =  init_dict(classIII, number, classIII_dict )
			classI_II_dict[classII] = classI
	return classI_dict,classII_dict,classIII_dict,classI_II_dict


def init_dict( key, value, dict):
	'''
    将字典值进行加和
    '''
	if key not in dict:
		dict[key] = 0
	dict[key] += value
	return dict

def write_file( dict, outfile, sample):
	flag = 0
	head = ['ClassI',sample]
	with open( outfile, 'w' ) as output:
		output.write( '\t'.join( head) + '\n')		
		for key in sorted(dict.keys()):
			flag += 1
			value = str(dict[key])
			out_line = [ str(flag), key, value]
			output.write( '\t'.join( out_line) + '\n')		

def write_classII( dict, outfile, I_II_dict, sample):
	flag = 0
	head = ['ClassII','ClassI',sample]
	with open( outfile, 'w' ) as output:
		output.write( '\t'.join( head) + '\n')		
		for key in sorted(dict.keys()):
			flag += 1
			value = str(dict[key])
			if key in I_II_dict:
				classI = I_II_dict[key]
			out_line = [ key,classI, value]
			output.write( '\t'.join( out_line) + '\n')		



def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--infile',help='anno file',dest='infile',required=True)
	parser.add_argument('-o','--outdir',help='outdir',dest='outdir',required=True)
	parser.add_argument('-p','--prefix',help='prefix',dest='prefix',required=True)
	args=parser.parse_args()

	classI_dict,classII_dict,classIII_dict, classI_II_dict = read_infile(args.infile)

	my_log.info("输出路径: {0}".format(args.outdir))
	outfileI = '{0}/{1}.classI.xls'.format( args.outdir, args.prefix)
	write_file(classI_dict, outfileI)
	
	outfileII = '{0}/{1}.classII.xls'.format( args.outdir, args.prefix, classI_II_dict)
	write_classII(classII_dict, outfileII)

	#outfileIII = '{0}/{1}.classIII.xls'.format( args.outdir, args.prefix)
	#write_file(classIII_dict, outfileIII)

if __name__ == '__main__':
	my_log = Log(filename)
	main()
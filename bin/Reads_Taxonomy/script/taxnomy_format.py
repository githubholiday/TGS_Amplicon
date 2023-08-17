'''
输入文件：
taxnomy.tsv文件
输出文件：
按照样本输出各样本的不同层级物种注释上的reads数量以及按照要求输出等级的物种百分比
参数：
-t:输出哪个等级的物种百分比,可选：kingdom,division,class,order ,family,genus,species，依次为 界、门、纲、目、科、属、种
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

def deal_taxnomy( tax_dic, tax_str, sample_info ):
	sample_num = len(sample_info)
	tax_list_tmp = tax_str.split(';')
	tax_list = [i.replace(" ","") for i in tax_list_tmp]
	kingdom = tax_list[0]
	division = '|'.join(tax_list[0:2])
	class_name = '|'.join(tax_list[0:3])
	order = '|'.join(tax_list[0:4])
	family = '|'.join(tax_list[0:5])
	genus = '|'.join(tax_list[0:6])
	species = '|'.join(tax_list[0:7]) #tax_str
	new_tax_list = [kingdom,division, class_name, order,family,genus,species  ]
	for tax in new_tax_list :
		if tax not in tax_dic:
			tax_dic[tax] = [0]*sample_num
		tax_sample_num_list = tax_dic[tax]
		tax_sample_info  = [i+j for i,j in zip(tax_sample_num_list,sample_info )]
		tax_dic[tax] = tax_sample_info
	return tax_dic

def get_taxnomy_dic( input):
	'''
    从输入文件中获取每个样本的物种对应丰度
    '''
	taxnomy_dic = {}
	sample_list = []
	with open( input, 'r') as infile:
		for line in infile:
			if line.startswith('#') : continue
			tmp = line.rstrip().split('\t')
			if line.startswith('id'):
				taxonomy = tmp[2]
				sample_list = tmp[4:]
				continue
			taxonomy = tmp[2]
			sample_info = [int(i) for i in tmp[4:]]
			taxnomy_dic = deal_taxnomy( taxnomy_dic, taxonomy, sample_info )
	return taxnomy_dic, sample_list    

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input of taxnomy',dest='input',required=True)
	parser.add_argument('-o','--outdir',help='outdir,default=indir',dest='outdir',required=True)
	parser.add_argument('-t','--type',help='type of class,choose from [domain,division,class,order,family,genus,species]',dest='type',default='species')
	args=parser.parse_args()
	
    #参数判断
	relation_dict = {'domain':'d__','division':'d__','class':'c__','order':'o__' ,'family':'f__','genus':'g__','species':'s__'}
	if args.type not in relation_dict:
		my_log.error("参数提供错误 -t:可选项为domain,division,class,order,family,genus,species")
		sys.exit(1)
	else:
		required_type = relation_dict[args.type]

    #获取不同等级物种的丰度	
	taxnomy_dic, sample_list = get_taxnomy_dic(args.input)
			
	for sample_index,sample in enumerate(sample_list) :
		output = '{0}/{1}.format.xls'.format( args.outdir,sample )
		output_species_stat = '{0}/{1}.species.rate.xls'.format( args.outdir,sample )
		species_read_count = 0 
		head = [ 'Sample',sample]
		with open( output, 'w') as outfile, open(output_species_stat, 'w') as ratefile :
			outfile.write("\t".join(head)+'\n')
			ratefile.write("Species\tReadNum\tReatCount\n")
			for tax in taxnomy_dic:
				tax_info = taxnomy_dic[tax]
				sample_tax_num = str(tax_info[sample_index])
				out_value = [tax, sample_tax_num]
				outfile.write('\t'.join(out_value)+'\n')
				if required_type in tax:
					species_read_count += tax_info[sample_index]
			#for tax in taxnomy_dic:
				#if required_type in tax:
					tax_info = taxnomy_dic[tax]
					species = tax.split("|"+required_type)[1]
					sample_tax_num = tax_info[sample_index]
					rate = '{0:.3f}'.format(sample_tax_num/species_read_count)
					out = [species, str(sample_tax_num),rate]
					ratefile.write('\t'.join(out)+'\n')
	my_log.info("输出文件为：1){0}/*format.xls\n2){0}/*species.rate.xls".format( args.outdir))
if __name__ == '__main__':
	my_log = Log(filename)
	main()

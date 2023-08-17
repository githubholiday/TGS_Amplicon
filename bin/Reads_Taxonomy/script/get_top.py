import sys
import argparse
import os
import datetime
from collections import defaultdict, OrderedDict
bindir = os.path.abspath(os.path.dirname(__file__))
filename=os.path.basename(__file__)

__author__ = "liaorui"
__mail__ = "ruiliao@genome.cn"

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


def get_dic(infile):
	'''
    获取到物种与丰度的字典
    key:str,s__Escherichia_coli
    value:int,丰度
    '''
	dic = {}
	spec = {}
	with open(infile,'r') as input:
		for line in input:
			if line.startswith('Sample'):continue
			tmp = line.strip().split("\t")
			tax_name = tmp[0].split('|')[-1]
			richness = int(tmp[1])
			dic[tax_name] = richness
	return dic

def get_top(sample_dic,top,spec_type):
	'''
    获取每个样本的前top个物种及物种丰度信息
    spec_type:d__,s__这些
    '''
	specise_dic = {}
	species_list = []
	for taxnomy in sample_dic:
		if taxnomy.startswith(spec_type):
			specise_dic[taxnomy] = sample_dic[taxnomy]
	top_dic = sorted( specise_dic.items(), key=lambda x:x[1], reverse=True)[0:top]
	for ss in top_dic:
		species = ss[0]
		if species not in species_list:
			species_list.append(species)
	return species_list

def write_top_species(all_sample_dic,top_species,outfile,sample_list, spec_type):
	'''
	按照物种(Species)将其对应的前top按照样本输出到文件中
	all_sample_dic:所有样本对应的物种以及其丰度字典，key=sample,value={"d_bacteria":3}
	top_species:筛选的所有物种的前n名物种的列表，['p__Actinobacteriota',p__Deinococcota]
	outfile:输出文件
	sample_list:样本列表
	spec_type:物种大类名，如domain,species等
	'''
	with open(outfile,'w') as out1:
		out1.write(spec_type.capitalize()+"\t"+"\t".join(sample_list)+"\n")
		for species in top_species:
			#print(species)
			count_list = []
			for sample in sample_list:
				#print(all_sample_dic[sample])
				if species not in all_sample_dic[sample]:
					count_list.append("0")
					#print('0')
				else:
					count_list.append(all_sample_dic[sample][species])
			out_value = [species]+[str(i) for i in count_list]
			out1.write("\t".join(out_value)+"\n")

def get_spenum(all_sample_dic,class_prefix,output,sample_list,spec_type):
	'''
    按照物种(Species)将其对应的前top按照样本输出到文件中
	all_sample_dic:所有样本对应的物种以及其丰度字典，key=sample,value={"d_bacteria":3}
	class_prefix:物种前缀名，如p__,s__
	output:输出文件句柄，已打开
	sample_list:样本列表
	spec_type:物种大类名，如domain,species等
    '''
	count_list = []
	for sample in sample_list:
		#index_name = [x for x in all_sample_dic if sample in x][0]
		count = 0
		if sample in all_sample_dic:
			for taxnomy_name in all_sample_dic[sample]:
				if taxnomy_name.startswith(class_prefix):
					count+=1
		count_list.append(count)
	out_value = [ spec_type.capitalize()] + [str(i) for i  in count_list]
	output.write("\t".join(out_value)+"\n")

def main():
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='the input file of braken report,required ',dest='input',nargs='+',required=True)
	
	parser.add_argument('-t','--top',help='top number',dest='top',type=int,required=True)
	parser.add_argument('-c','--class',help='class of species,choose from [domain,division,class,order,family,genus,species]',dest='cla',default='species',required=False)
	parser.add_argument('-o','--outdir',help='output file,norequired',dest='outdir',required=True)
	parser.add_argument('-p','--prefix',help='prefix of the output',dest='prefix',required=True)
	args=parser.parse_args()

	relation_dict = OrderedDict()
	relation_dict = {'domain':'d__','division':'p__','class':'c__','order':'o__' ,'family':'f__','genus':'g__','species':'s__'}
	species_list = ['domain','division','class','order','family','genus','species']
	if args.cla in relation_dict :
		tax_name = relation_dict[args.cla]
	else:
		my_log.error("-c 参数提供错误")
		sys.exit(1)
	if args.top <= 0 :
		my_log.error("-t参数错误,必须为正整数")
		sys.exit(1)
	
	all_dic = {} #所有样本的物种及丰度信息,key=样本，value={d_bacteria:丰度}
	top_species_dict = {}
	species = []
	sample_list = []
	for infile in args.input:
		file_name = os.path.basename(infile).split('.')[0]
		sample_name = file_name.split('.')[0]
		sample_list.append(sample_name)
		if filename not in all_dic:
			all_dic[sample_name] = {}
			#sample_dic = all_dic[sample_name]
		all_dic[sample_name] = get_dic(infile)
		#print(sample_dic)
		
		#species.extend(list(sample_dic.keys()))
		#获取每个样本的每个物种级别的前n个的名称,按照类别存入到top_species_dict=[s__Rhodobacter_sphaeroides,s__Escherichia_coli]中
		for class_name in relation_dict:
			class_prefix = relation_dict[class_name]
			if class_name not in top_species_dict:
				top_species_dict[class_name] = []
			sample_top_species = get_top(all_dic[sample_name],args.top,class_prefix)
			for species in sample_top_species:
				if species not in top_species_dict[class_name]:
					top_species_dict[class_name].append(species)
			#top_species示例 [d__bacteria,s__Pseudomonas_aeruginosa]
	all_sample_stat = args.outdir+"/Species_count.xls"
	with open(all_sample_stat,'w') as out:
		out.write("Sample\t"+"\t".join(sample_list)+"\n")
		index = 0
		#for class_name in relation_dict:
		for class_name in species_list:
			class_prefix = relation_dict[class_name]
			get_spenum(all_dic,class_prefix,out,sample_list,class_name)
			#输出前n名物种及丰度 表
			if class_name == 'domain': continue
			index += 1
			top_species = sorted(set(top_species_dict[class_name])) #每个物种所有样本的前n名物种列表
			top_file = "{0}/{1}_{2}_{3}_{4}_top.xls".format(args.outdir,args.prefix,str(index),class_name,str(args.top)) #richness_6_Species_10_top.xls
			my_log.info("输出文件: {0}".format(top_file))
			write_top_species(all_dic,top_species,top_file,sample_list,class_name)
	my_log.info("输出文件: {0}".format(all_sample_stat))
if __name__ == "__main__":
	my_log = Log(filename)
	main()

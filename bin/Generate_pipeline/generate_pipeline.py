#! /usr/bin/env python3
import argparse
import sys
import os
import re
import datetime
import glob
import json
import configparser
import math

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

class myconf(configparser.ConfigParser):
	def __init__(self, defaults=None):
		configparser.ConfigParser.__init__(self, defaults=None, allow_no_value=True)

	def optionxform(self, optionstr):
		return optionstr

def my_mkdir( dir_list ):
	for each_dir in dir_list :
		if not os.path.exists(each_dir) :
			os.makedirs( each_dir )

def my_run( cmd ):
	if os.system( cmd) == 0 :
		my_log.info("执行成功：{0}".format( cmd ))
	else :
		my_log.info("执行失败，退出:{0}".format( cmd ))
		sys.exit(1)

def read_config( config_file ):
	'''
	读取流程配置文件，获取软件等信息
	'''
	config_dic = {}
	with open(config_file, 'r') as infile:
		for line in infile:
			if line.startswith('#'):continue
			if line.strip() == '' : continue
			tmp = line.rstrip().split('=',1)
			key = tmp[0]
			value = tmp[1]
			if key in config_dic :
				my_log.error("{0} 在config文件中重复".format(key))
				sys.exit(1)	
			else :
				config_dic[key] = value
	return config_dic
		
# ====== 公共模块 =================================

# ====== 信搜处理模块 =================================
def get_info_file( info_dir ):
	'''
    获取信息收集表文件，如果无或者超过1个，都会报错退出
    '''
	info_file = glob.glob( info_dir+'/*')
	if len(info_file) == 0 :
		my_log.error("{0} 目录下没有信息收集表文件，退出".format( info_dir))
		sys.exit(1)
	elif len(info_file) > 1:
		my_log.error("{0} 目录下有多个信息收集表文件，退出".format( info_dir))
		sys.exit(1)
	else:
		return info_file[0]

def read_info_file( info_file, info_json, info_conf ,table2json_script):
	'''
    使用脚本直接获取信息收集表内容，并输出到info_json文件中
    参数：
    info_file:[输入]信息收集表
    info_conf:[输入]信息收集表配置文件，需要转化的内容配置
    info_json:[输出]信息收集表转化后的json文件
    table2json_script:[脚本]转化表格为Json的脚本（rust)编写的，作者刘涛
    '''	
	cmd = '{0} -c {1} -x {2} -j {3}'.format( table2json_script, info_conf, info_file, info_json)
	my_run( cmd )

def get_env_file(info_dir):
	'''
    获取环境因子文件
    '''	
	env_file = '{0}/enviroment.txt'.format( info_dir)
	enviroment = ''
	if not os.path.exists( env_file) :
		my_log.warning("没有环境因子文件:{0} 不存在,不做环境因子分析 ".format(env_file))
		enviroment = ''
	else:
		enviroment = env_file
	return enviroment
		
# ====== 信搜处理模块 =================================

class Pipe_Info():
	def __init__( self, info_conf, analysis_dir, config_dic, filter_dir, env_file, read_count ):
		self.info_conf = info_conf
		self.analysis_dir = analysis_dir
		self.config_dic = config_dic
		self.filter_dir = filter_dir
		self.env_file = env_file
		self.read_count = read_count
		self.sample_list = '{0}/sample.list'.format( self.analysis_dir )
		self.config_file = '{0}/config.ini'.format( self.analysis_dir )
		self.cmp_file = '{0}/cmp.txt'.format( self.analysis_dir )
		self.group_file = '{0}/group.txt'.format( self.analysis_dir )
		self.sample_csv = '{0}/prepare/sample.txt'.format( self.analysis_dir )
		self.meta_csv = '{0}/prepare/metadata.txt'.format( self.analysis_dir )
		self.config = myconf()
		self.load_json()
		self.get_group_file()
		self.sample_num = self.generate_pb_conf()
	
	def load_json( self ):
		json_file = open( self.info_conf, 'r')
		self.json_dic = json.load( json_file )
		self.sub_project_id = self.json_dic['sub_project_id']
		self.project_name = self.json_dic['project_name']
		self.analysis_type = self.json_dic['analysis_type']

	def get_group_file(self):
		group_dic =  self.json_dic['group_ip_input']
		with open( self.group_file, 'w') as outfile:
			for group in group_dic:
				out_value = [ group] + group_dic[group]
				outfile.write("\t".join(out_value)+'\n')
		
	def generate_pb_conf(self):
		'''
        生成Pb_16s 软件需要的meta和sample信息表
		'''
		sample_num = 0
		sample_info_dict = self.json_dic['samples']
		with open( self.sample_csv, 'w') as sample_out_file, open( self.meta_csv, 'w') as meta_out_file:
			sample_out_file.write("sample-id\tabsolute-filepath\n")
			meta_out_file.write("sample_name\tcondition\n")
			for sample in sample_info_dict:
				sample_num += 1
				group = sample_info_dict[sample][0][3]
				report_name = sample_info_dict[sample][0][1]
				out = [ report_name, group]
				meta_out_file.write('\t'.join(out)+'\n')
				
				fq_path = '{0}/Analysis/Merge_bam/{1}/{1}.hifi.fastq.gz'.format( self.analysis_dir,report_name)
				out_s = [report_name,fq_path ]
				sample_out_file.write('\t'.join(out_s)+'\n')
		return sample_num
	
	def default_para( self ):
		label_list = ['sample', 'cmp','Para']
		[self.config.add_section(i) for i in label_list]
	
	def config_sample( self ):
		'''
        获取config.ini文件中的sample（样本）信息，同时将样本信息输出到sample.list文件中，便于后期报告生成
        '''
		sample_info_dict = self.json_dic['samples']
		sample_list_file = open( self.sample_list, 'w')
		head = ["Sample","Group","Description"]
		sample_list_file.write('\t'.join(head)+'\n')
		for sample in sample_info_dict :
			sample_info = sample_info_dict[sample][0]
			sample_name = sample_info[1]
			sample_group = sample_info[3]
			sample_descibe = sample_info[2]
			sample_read_count = random_count(self.read_count, sample_name, rate=0.1)
			sample_info_str = '\t'.join([sample_name,sample_group,sample_descibe])
			sample_list_file.write(sample_info_str+'\n')
			config_sample_str = '\t'.join([sample,sample_name,sample_group,sample_descibe,str(sample_read_count)])
			self.config.set('sample',config_sample_str)
						
	def config_cmp( self) :
		'''
        获取config.ini文件中的cmp(比较组)信息
        '''
		cmp_info_list = self.json_dic['group_pair']
		cmp_file = open(self.cmp_file,'w')
		for each_cmp in cmp_info_list:
			cmp_str = '\t'.join(each_cmp)
			cmp_file.write(cmp_str+'\n')
			diff = self.judge_diff(each_cmp, cmp_str)
			cmp_str += '\t'+diff
			self.config.set('cmp',cmp_str)
			
	def judge_diff(self, cmp, cmp_str):
		'''
		判断是否能做差异分析
		条件：有比较组且每个比较组中有三个或三个以上样本
		'''
		cmp1 = cmp[0]
		cmp2 = cmp[1]
		group_dic =  self.json_dic['group_ip_input']
		if cmp1 in group_dic and cmp2 in group_dic :
			cmp1_sample = group_dic[cmp1]
			cmp2_sample = group_dic[cmp2]
			if len(cmp1_sample) >= 3 and len(cmp2_sample) >= 3:
				my_log.info("差异比较组可做差异分析:{0}".format(cmp_str))
				return "diff"
			else:
				my_log.info("差异比较组不做差异分析:{0}".format(cmp_str))
				return "no"	
		else:
			return "no"
			my_log.error("比较组中无样本信息:{0}".format(cmp_str))
	def get_private_para(self):
		'''
	    获取不同文库的长度、Primer、数据库等信息
		'''
		self.config.set('Para','Para_denoise_min_len',self.config_dic['{0}_denoise_min_len'.format(self.analysis_type)])
		self.config.set('Para','Para_denoise_max_len',self.config_dic['{0}_denoise_max_len'.format(self.analysis_type)])
		self.config.set('Para','Para_front_p_dada2',self.config_dic['{0}_front_p_dada2'.format(self.analysis_type)])
		self.config.set('Para','Para_tail_p_dada2',self.config_dic['{0}_tail_p_dada2'.format(self.analysis_type)])
		self.config.set('Para','Para_front_p_cutadap',self.config_dic['{0}_front_p_cutadap'.format(self.analysis_type)])
		self.config.set('Para','Para_tail_p_cutadap',self.config_dic['{0}_tail_p_cutadap'.format(self.analysis_type)])
		self.config.set('Para','Para_search_db',self.config_dic['{0}_search_db'.format(self.analysis_type)])
		self.config.set('Para','Para_search_db_tax',self.config_dic['{0}_search_db_tax'.format(self.analysis_type)])
		
    

	def config_para( self ):
		'''
        获取config.ini文件中的cmp(比较组)信息,可以根据流程需求随时添加
        '''
		pipe_config = os.path.abspath("{0}/../../config/config.txt".format(bindir))
		self.config.set('Para','Para_project_id',self.sub_project_id)
		self.config.set('Para','Para_project_name',self.project_name)
		self.config.set('Para','Para_outdir','{0}/Analysis'.format( self.analysis_dir))
		self.config.set('Para','Para_sample_list',self.sample_list)
		self.config.set('Para','Para_group_file',self.group_file)
		self.config.set('Para','Para_cmp',self.cmp_file)
		self.config.set('Para','Para_sample_csv',self.sample_csv)
		self.config.set('Para','Para_meta_csv',self.meta_csv)
		self.config.set('Para','Para_analysis_type',self.analysis_type)
		self.config.set('Para','Para_config',pipe_config)
		self.config.set('Para','Para_data_dir',self.filter_dir)
		self.config.set('Para','Para_env_file',self.env_file)
		self.get_private_para()
        
	def config_write( self ):
		self.default_para()
		self.config_sample()
		self.config_cmp()
		self.config_para()
		self.config.write( open(self.config_file, 'w'))
		my_log.info("config文件输出完成:{0}".format( self.config_file))

	def get_job_config(self):
		'''
		根据分析类型获取job_config文件
	    '''
		self.job_config = '{0}/../../config/{1}_job_config.txt'.format(bindir, self.analysis_type)
		if not os.path.exists( self.job_config ):
			my_log.error("文件不存在:{0},请确认分析类型是否正确：[16s,18s,ITs]，退出".format(  self.job_config  ))
			sys.exit(1)
			
	def generate_work_shell(self, run ):
		'''
        生成投递脚本
        '''
		self.get_job_config()
			
		python3 = self.config_dic['PYTHON3']
		generate_pipeline = self.config_dic['generate_pipeline']
		work_cmd = '{python3} {generate_pipeline} -i {self.job_config} -o {self.analysis_dir}/prepare/pipeline &&'.format(python3=python3, generate_pipeline=generate_pipeline,self=self )
		work_cmd += '\n{python3} {self.analysis_dir}/prepare/pipeline/pipeline.py -i {self.config_file} -j {self.sub_project_id}_micro -b {bindir}/../ -o {self.analysis_dir}/Analysis -name {self.sub_project_id}_micro -r\n'.format(python3=python3, self=self, bindir=bindir)
		
		work_shell = '{0}/{1}_qsub_sge.sh'.format( self.analysis_dir, self.sub_project_id)
		with open( work_shell, 'w') as outfile:
			outfile.write("#!/bin/bash\n")
			outfile.write(work_cmd)
			run_cmd = 'nohup /bin/bash {0} &'.format( work_shell )
			if run :
				my_run(run_cmd)
			else:
				my_log.info("请手动投递脚本:{0}".format( work_shell ))
				
def random_count( read_count, sample_name, rate=0.1 ):
	'''
	 根据每个样本的read_count，在read_count-read_count*(1+rate)之间随机取值
	'''
	import random
	read_count = int(read_count)
	random.seed(sample_name)
	random_read_count = math.ceil(read_count*(1+rate))
	random_count = random.randint(read_count, random_read_count)
	return random_count*4

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-c','--config',help='config_file',dest='config',default='{0}/../../config/config.txt'.format( bindir))
	parser.add_argument('-i','--indir',help='indir of analysis',dest='indir',required=True)
	parser.add_argument('-o','--outdir',help='outdir,default=indir',dest='outdir')
	parser.add_argument('--read_count',help='the read count of each sample',type=int, dest='read_count',default=10000)
	parser.add_argument('-r','--run',help='run or not',action='store_true')
	args=parser.parse_args()
	
    # 给参数赋值
	config_file = args.config
	indir = args.indir
	outdir = args.indir
	if args.outdir:
		outdir=args.outdir
	
	# 定义路径 - 输入
	filter_dir = '{0}/Filter/Filter_Result/ANNO_all_data'.format( indir )
	if not os.path.exists( filter_dir ):
		my_log.error("下机数据路径不存在，格式为Filter/Filter_Result/ANNO_all_data ")
	info_dir = '{0}/info'.format( indir )
	
	# 定义路径/文件 - 输出
	analysis_dir = '{0}/Analysis-test/'.format( outdir )
	prepare_dir = '{0}/prepare'.format( analysis_dir )
	my_mkdir( [analysis_dir, prepare_dir])
    # 读取配置文件
	config_dic = read_config(config_file)
	
    # 获取信息收集表文件 并将表格信息读取到info_json文件中
	info_file = get_info_file(info_dir)
	info_json = '{0}/info.json'.format( prepare_dir)
	info_conf = '{0}/config.json'.format( bindir)
	table2json_script = config_dic["table2json"]
	read_info_file( info_file, info_json, info_conf, table2json_script )
	
    # 获取环境因子文件
	env_file = get_env_file(info_dir)

    # 获取项目的config.ini文件以及投递脚本
	my_pipe = Pipe_Info(info_json, analysis_dir, config_dic, filter_dir, env_file, args.read_count)
	my_pipe.config_write()
	my_pipe.generate_work_shell( args.run)

if __name__ == '__main__':
	my_log = Log(filename)
	main()
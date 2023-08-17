'''
输入文件要求：
1）一列为值，该列的列名就是-l参数
2）一列为组名，必须为Group

示例：
/annoroad/data1/software/install/Miniconda/Anaconda3-2021.05/envs/assembly/bin/python3 ../../script/de_boxplot.py -i infile.txt -o bo.pdf -l ACE

'''

#!/usr/bin/evn python3
######################################################################### import ##########################################################
import argparse
import os
import sys
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statannot import add_stat_annotation
import itertools
######################################################################### ___  ##########################################################
__author__ = 'Tu chengfang'
__mail__ = 'chengfang@genome.cn'
__date__ = '2023-5-6'
__version__ = '1.0'
######################################################################### main  ##########################################################
def plot_number_boxplot(df,x,y,pairs,test_method,outfile):
	'''
	绘制带有显著性的boxplot图
	'''
	plt.figure(figsize=(5,5))
	g=sns.boxplot(data=df,x=x,y=y, linewidth=0.8,fliersize=1) #showfliers=False
	add_stat_annotation(ax=g,data=df,x=x,y=y,test=test_method,loc="inside",verbose=2,box_pairs=pairs)
	plt.tight_layout()
	plt.savefig(outfile)
	plt.close()

def get_cmp( group, num=3 ):
	'''
	将df中的group列获取后，判断组数量是否超过给定数量，如果超过，则取num个组，并将组进行两两组合
	group:df.array
	'''
	group_list = []
	group_final = []
	for g in group:
		if g not in group_list :
			group_list.append(g)
	if len(group_list) > num :
		group_final=group_list[0:num]
	else:
		group_final = group_list
		
	cmp = list(itertools.combinations(group_final,2))
	return cmp
def redef_df(df, cmp_list):
	'''
    按照指定的组名重新获取df数据
    '''
	dfs = []
	for cmp in cmp_list:
		g1 = cmp[0]
		g2 = cmp[1]
		data1 = df[df['Group'] == g1]
		dfs.append(data1)
		data2 = df[df['Group'] == g2]
		dfs.append(data2)
		
	df_o = pd.concat(dfs)
	return df_o

def main():
	function="this program is used to "
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='author:\t{0}\nmail:\t{1}\ndate:\t{2}\nversion:\t{3}\nfunction:\t{4}'.format(__author__,__mail__,__date__,__version__,function))
	parser.add_argument('-i',help='input ICGC file',dest='infile',type=str,required=True)
	parser.add_argument('-l',help='label of the value column name',dest='label',type=str,required=True)
	parser.add_argument('-o',help='output file',type=str,dest='outfile',required=True)
	parser.add_argument('-t',help='test method,default:t-test_ind',type=str,dest='test_method',default='t-test_ind')
	parser.add_argument('-n',help='the num of group to plot',type=int,dest='num',default=3)
	args=parser.parse_args()
	#读取文件
	df=pd.read_csv(args.infile,header=0,sep='\t')
	#获取比较组信息
	cmp_list = get_cmp( df.Group) #文件的组列必须为group
	data = redef_df( df, cmp_list)
	y = args.label
	x = 'Group' 
	plot_number_boxplot(data,x,y,cmp_list, args.test_method, args.outfile)
if __name__=="__main__":
	main()
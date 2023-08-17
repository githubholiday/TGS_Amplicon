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
######################################################################### ___  ##########################################################
__author__ = 'Tu chengfang'
__mail__ = 'chengfang@genome.cn'
__date__ = '2023-5-6'
__version__ = '1.0'
######################################################################### main  ##########################################################
def plot_number_boxplot(df,outfile):
	pdf=outfile
	plt.figure(figsize=(8,5))
	g=sns.boxplot(data=df,x="group",y="ACE")
	add_stat_annotation(ax=g,data=df,x="group",y="ACE",test="t-test_ind",loc="inside",verbose=2,box_pairs=[("A","B"),('B','C'),('A','C')])

	#plt.legend(bbox_to_anchor=(1.02,0.8),ncol=1,loc='upper left')
	#plt.ylim(ymax=400)
	plt.tight_layout()
	plt.savefig(pdf)
	plt.close()


def main():
	function="this program is used to "
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='author:\t{0}\nmail:\t{1}\ndate:\t{2}\nversion:\t{3}\nfunction:\t{4}'.format(__author__,__mail__,__date__,__version__,function))
	parser.add_argument('-i',help='input ICGC file',type=str,required=True)
	parser.add_argument('-l',help='label of the value column name',type=str,required=True)
	parser.add_argument('-o',help='output file',type=str,required=True)
	args=parser.parse_args()
	dt=pd.read_csv(args.i,header=0,sep='\t')
	plot_number_boxplot(dt,args.o)
if __name__=="__main__":
	main()

#! /usr/bin/env python3

import argparse
import os
import sys
import re
import json

__author__='huayunyun lee'
__mail__='huayunli@genome.cn'
__doc__=''


def read_file(file):
	if os.path.exists(file):
		with open(file,'r')as fl:
			for line in fl:
				if not line.strip(''):continue
				yield line.strip('\n')
	else:
		print ("file {0} didn't exist!".format(file))


def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-j','--json',help='ccs qc json file(ccs.report.json)',dest='rj',required=True)
	parser.add_argument('-n','--name',help='sample name',dest='name',required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',required=True)

	args=parser.parse_args()
	###############参数梳理###############
	rj, name, output = args.rj, args.name, args.output
	###############获取ms文件列表##############
	# json.text文件的格式： [{"a":1},{"a":2},{"a":3},{"a":4},{"a":5}]
	# 获取ｊｓｏｎ数据
	with open(rj , 'r', encoding='utf-8') as f:
		rows = json.load(f)
		ccs_rawstat = rows["attributes"]
		out_line = "Sample" + "\t" + name + "\n"
		for term in ccs_rawstat:
			if term["id"] not in ["ccs2.number_of_ccs_reads","ccs2.total_number_of_ccs_bases","ccs2.mean_ccs_readlength","ccs2.median_accuracy"]: continue
			if term["name"] == "HiFi Reads" or term["name"] =="HiFi Yield (bp)" or term["name"] =="HiFi Read Length (mean, bp)":
				out_line = out_line + str(term["name"]) + "\t" + str(format(term["value"],",")) + "\n"
			else:
				out_line = out_line + str(term["name"]) + "\t" + str(term["value"]) + "\n"
	with open(output,"w")as ot:
		ot.write(out_line)


if __name__ == '__main__':
	main()

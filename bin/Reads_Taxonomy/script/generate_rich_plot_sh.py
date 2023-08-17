import sys
import argparse
import os
os.environ['OPENBLAS_NUM_THREAD'] = '1'
__author__ = "liaorui"
__mail__ = "ruiliao@genome.cn"

def main():
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='the input file of braken report,required ',dest='input',nargs='+',required=True)
	parser.add_argument('-o','--output',help='output file,norequired',dest='output',required=True)
	parser.add_argument('--Rscript',dest='Rscript',required=False)
	parser.add_argument('--convert',dest='convert',required=False)
	parser.add_argument('-r',help="绘图脚本",dest='rplot',required=False)
	args=parser.parse_args() 
	with open( args.output, 'w') as outfile:
		for each_file in args.input :
			
			prefix = each_file.split(".xls")[0]
			
			cmd = 'export OPENBLAS_NUM_THREADS=2 && {Rscript} {plot_r} {infile} {prefix}.pdf F\n'.format(Rscript=args.Rscript, plot_r=args.rplot, infile=each_file, prefix=prefix )
			cmd += '{convert} {prefix}.pdf {prefix}.png\n'.format( convert=args.convert, prefix=prefix)
			outfile.write(cmd)
	print("请运行 {0}".format( args.output ))
 	


if __name__ == "__main__":
	main()

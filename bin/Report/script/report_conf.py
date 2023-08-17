##### cat report_conf.py
#! /usr/bin/env python3
import argparse
import sys
import os
import re
import time
import logging
import configparser
bindir = os.path.abspath(os.path.dirname(__file__))
pat=re.compile('^\s$')
pat2 = re.compile('\[(\S+)\]')


__author__='tu chengfang'
__mail__= 'chengfangtu@genome.cn'

now = time.strftime("%Y-%m-%d %H:%M:%S")
LOG = os.path.basename(__file__)

def my_log( level, message ) :
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    if level == 'info' :
        return logger.info( message )
    if level == 'warning' :
        return logger.warning( message )
    if level == 'debug' :
        return logger.debug( message )
    if level == 'error' :
        return logger.error( message )

def check_file_exists( *file_list ) :
    for file in file_list :
        if os.path.exists( file ) :
            my_log( 'info', 'file : {0}'.format( file ) )
        else :
            my_log( 'error', 'file is not exists : {0}'.format( file ) )

def make_dir( dir ) :
    if not os.path.exists( dir ) :
        try :
            os.makedirs( dir )
            time.sleep(1)
            my_log( 'info', 'mkdir {0} sucessful!'.format( dir) )
        except :
            my_log( 'error', 'mkdir {0} failed!'.format( dir) )
    else :
        my_log( 'info', '{0} is exist'.format( dir ) )

def myrun( cmd ) :
    if os.system( cmd ) == 0 :
        my_log( 'info', '{0} run sucessfully !'.format( cmd ) )
    else :
        my_log( 'error', '{0} run failed !'.format( cmd ) )

class myconf(configparser.ConfigParser):
	def __init__(self, defaults=None):
		configparser.ConfigParser.__init__(self, defaults=None, allow_no_value=True)

	def optionxform(self, optionstr):
		return optionstr



def main():
    parser=argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
    parser.add_argument('-c','--config',help='config file',dest='config',required=True)
    parser.add_argument('-o','--output',help='output file',dest='output',required=True)
    parser.add_argument('-u','--upload',help='upload dir',dest='upload',required=True)
    args=parser.parse_args()

    conf = myconf(  )
    conf.read(args.config)

    project_name = conf['Para']['Para_project_name']
    project_id = conf['Para']['Para_project_id']

    with open( args.output,'w') as outfile:
        outfile.write("PROJECT_NAME:{0}结题报告\n".format( project_name))
        outfile.write("PROJECT_ID:{0}\n".format( project_id))
        outfile.write("REPORT_DIR:{0}".format( args.upload))


if __name__ == '__main__':
    main()
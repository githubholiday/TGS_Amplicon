makefile_dir=$(dir $(firstword $(MAKEFILE_LIST)))
makefile_name=$(notdir $(firstword $(MAKEFILE_LIST)))
script=$(makefile_dir)/script/

ifdef config
	include $(config)
else
	include $(makefile_dir)/software/software.txt
endif

HELP:
	@echo Description: 原始过滤
	@echo Program: filter.mk
	@echo Version: v1.0.0
	@echo Contactor: chengfangtu@genome.cn
	@echo CutAdapt:对数据进行去除接头，如果数据不包含接头将其丢掉
	@echo -e "\t" "make -f $(makefile_name) infq= front= tail= outfq= outjson= cpu= software= CutAdapt"
	@echo 参数说明：
	@echo -e "\t" "software: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/software/software.txt "
	@echo -e "\t" "infq:  [文件|必需]  输入fastq文件"
	@echo -e "\t" "front_p: [字符串|必需]5'端的引物序列"
	@echo -e "\t" "tail_p:  [字符串|必需]3'端的引物序列"
	@echo -e "\t" "outfq: [文件|必需]  输出fastq文件"
	@echo -e "\t" "outjson: [文件|必需]输出json文件,统计文件"
	@echo -e "\t" "cpu:   [文件|必需]  线程数"

front_p=AGRGTTYGATYMTGGCTCAG
#tail_p=RGYTACCTTGTTACGACTT
tail_p=AAGTCGTAACAAGGTARCY
cutadapt_cpu=3
outdir=$(dir $(firstword $(outfq)))
.PHONY:CutAdapt
CutAdapt:
	echo "############### CutAdapt start at `date` ###############"
	mkdir -p $(outdir)
	$(CUTADAPT) -g "$(front_p)...$(tail_p)" $(infq) -o $(outfq) -j $(cutadapt_cpu) --trimmed-only --revcomp -e 0.1 --json $(outjson)
	echo "############### CutAdapt end at `date` ###############"

cutadapt_stat:
	echo "############### cutadapt_stat start at `date` ###############"
	$(PYTHON3) $(script)/stat_filter.py -i $(cutadapt_json) -s $(sample) -o $(outfile)
	echo "############### cutadapt_stat end at `date` ###############"

collect_stat:
	echo "############### collect_stat start at `date` ###############"
	$(CSVTK) concat -t -C "%" $(infile) > $(outfile)
	echo "############### collect_stat end at `date` ###############"


fq_stat:
	echo "############### fq_stat start at `date` ###############"
	$(SEQKIT) fx2tab -j $(cpu) -q --gc -l -H -n -i $(infq) |$(CSVTK) mutate2 -C '%' -t -n sample -e '"${sample}"' > ${outfile}

collect_fq_stat:
	echo "############### collect_fq_stat start at `date` ###############"
	$(CSVTK) concat -t -C '%' $(infile) > $(outfile)
	echo "############### collect_fq_stat end at `date` ###############"





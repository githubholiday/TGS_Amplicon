BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)
file=$(abspath $(firstword $(MAKEFILE_LIST)))
threads?=10
top?=10
kmer?=100

alignment_dir=$(outdir)/assemble/$(sample)

Help:
	@echo Description:
	@echo -e "\t" 该脚本用于数据基础统计以及长度绘图
	@echo -e "\t" Author "\t": chengfangtu
	@echo target:
	@echo -e "\t filter_stat:使用cutadapter后的read统计文件进行所有样本reads的长度信息"
	@echo -e "\t make -f $(file) read_stat= sample_stat= ccs_stat= outdir= config= filter_stat"
	@echo -e "\t read_stat : pb-tools输出的cutadater后的read的统计文件:all_samples_seqkit.readstats.post_trim.tsv"
	@echo -e "\t sample_stat : pb-tools输出的cutadater后的样本reads数据量的统计文件:all_samples_cutadapt_stats.tsv"
	@echo -e "\t ccs_stat : 下机数据的ccs统计文件"
	@echo -e "\t len_stat: reads按照长度区间进行统计和绘图"
	@echo Usage:
	@echo -e "\t" make -f $(file) read_stat=  sample_list= stat_conf= outdir= config= len_stat
	@echo Parameters:
	@echo -e "\t read_stat : pb-tools输出的cutadater后的read的统计文件:all_samples_seqkit.readstats.post_trim.tsv"
	@echo -e "\t sample_list : 样本列表，第一列为样本名称"
	@echo -e "\t stat_conf : 长度区间配置文件，为模块 config/stat.conf文件"
	@echo -e "\t outdir: 结果输出路径"

filter_stat:
	@echo "===================== Run filter_stat Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(CSVTK)  summary -t -C '%' -g sample -f length:mean $(read_stat) >> $(outdir)/sample_len.xls
	$(CSVTK) -t join -f 1 $(sample_stat) $(outdir)/sample_len.xls > $(outdir)/sample_raw_stat.xls
	$(PYTHON3) $(BIN)/script/filter_stat.py -i $(ccs_stat) -l $(outdir)/sample_raw_stat.xls -o $(outdir)/sample_stat.xls
	@echo "===================== Run filter_stat End at `date` ===================== "

len_stat:
	@echo "===================== Run filter_stat Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/len_stat.py -i $(read_stat) -s $(sample_list) -c $(stat_conf) -o $(outdir)
	@echo "===================== Run filter_stat End at `date` ===================== "




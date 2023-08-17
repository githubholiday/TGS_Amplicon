makefile_dir=$(dir $(firstword $(MAKEFILE_LIST)))
makefile_name=$(notdir $(firstword $(MAKEFILE_LIST)))
script=$(makefile_dir)/script/

ifdef config
	include $(config)
else
	include $(makefile_dir)/software/software.txt
endif

HELP:
	@echo Description:将数据进行ASV处理以及物种注释
	@echo Program: asv.mk
	@echo Version: v1.0.0
	@echo Contactor: chengfangtu@genome.cn

	@echo ImportQiime: 将样本列表导入为qza格式
	@echo -e "\t" "make -f $(makefile_name) sample_list= out_qza= software= ImportQiime"
	@echo 参数说明：
	@echo -e "\t" "software: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/software/software.txt "
	@echo -e "\t" "sample_list: [文件|必需] 样本与对应fq路径的以tab分割的文件,表头为sample-id\tabsolute-filepath,第二行为样本名\tfq绝对路径"
	@echo -e "\t" "out_qza:  [字符串|必需]导出的qza文件"
	@echo -e "\t" "outfq: [文件|必需]  输出fastq文件"

	@echo Denoise: 使用dada2-denoise进行降噪并生成asv表(使用原始数据，并不是cutadapt的数据)
	@echo -e "\t" "make -f $(makefile_name) sample_qza= out_table_qza= out_rep_qza= out_stat_qza= denoise_min_len= denoise_max_len= denoise_max_ee= front_p= tail_p= cpu= denoise_pooling_method= software= Denoise"
	@echo 参数说明：
	@echo -e "\t" "输入："
	@echo -e "\t" "software: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/software/software.txt "
	@echo -e "\t" "sample_qza: [文件|必需] fastq文件列表导入的qza文件，为ImportQiime的输出"
	@echo -e "\t" "参数："
	@echo -e "\t" "denoise_min_len:[字符串|可选]ASV序列的最小长度，默认为1000"
	@echo -e "\t" "denoise_max_len:[字符串|可选]ASV序列的最大长度，默认为1600"
	@echo -e "\t" "denoise_max_ee: [字符串|可选]ASV序列的最大期望错误，默认为2"
	@echo -e "\t" "front_p: [字符串|可选]前端引物，默认为AGRGTTYGATYMTGGCTCAG"
	@echo -e "\t" "tail_p: [字符串|可选]后端引物，默认为RGYTACCTTGTTACGACTT"
	@echo -e "\t" "cpu: [字符串|可选]线程数，默认为10"
	@echo -e "\t" "denoise_pooling_method: [字符串|可选]池化方法，默认为pseudo"
	@echo -e "\t" "输出："
	@echo -e "\t" "out_freq_qza: [字符串|必需]ASV频率输出文件，qza格式"
	@echo -e "\t" "out_rep_qza: [字符串|必需]ASV序列输出文件，qza格式,导出是fasta格式"
	@echo -e "\t" "out_stat_qza: [字符串|必需]ASV统计输出文件，qza格式"
	
outdir=$(dir $(firstword $(out_qza)))
ImportQiime:
	echo "############### ImportQiime start at `date` ###############"
	mkdir -p $(dir $(firstword $(out_qza)))
	$(QIIME2) tools import --type 'SampleData[SequencesWithQuality]'  --input-path $(sample_list) --output-path $(out_qza) --input-format SingleEndFastqManifestPhred33V2
	echo "############### ImportQiime end at `date` ###############"

denoise_pooling_method=pseudo
denoise_min_len=1000
denoise_max_len=1600
denoise_max_ee=2
cpu=10
front_p=AGRGTTYGATYMTGGCTCAG
tail_p=RGYTACCTTGTTACGACTT
outdir=$(dir $(firstword $(out_table_qza)))
Denoise:
	echo "############### Denoise start at `date` ###############"
	mkdir -p $(outdir)
	source $(conda_activate) $(qiime2_env)
	$(QIIME2) dada2 denoise-ccs --i-demultiplexed-seqs $(sample_qza) \
	--o-table  $(out_freq_qza) \
	--o-representative-sequences $(out_rep_qza) \
	--o-denoising-stats $(out_stat_qza)\
	--p-min-len $(denoise_min_len) --p-max-len $(denoise_max_len) \
	--p-max-ee $(denoise_max_ee) \
	--p-front $(front_p) \
	--p-adapter $(tail_p) \
	--p-n-threads $(cpu) \
	--p-pooling-method '$(denoise_pooling_method)'
	echo "############### Denoise end at `date` ###############"

qza_export:
	echo "############### export_qza start at `date` ###############"
	$(QIIME2) tools export --input-path $(inqza) --output-path $(outdir)
	echo "############### export_qza end at `date` ###############"

export_asv:
	echo "############### export_asv_fa_frep start at `date` ###############"
	$(QIIME2) tools export --input-path $(asv_freq) --output-path $(outdir)/asv_freq
	$(QIIME2) tools export --input-path $(asv_rep) --output-path $(outdir)/asv_rep
	$(QIIME2) tools export --input-path $(asv_stat) --output-path $(outdir)/asv_stat
	echo "############### export_asv_fa_frep end at `date` ###############"
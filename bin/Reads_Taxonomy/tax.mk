makefile_dir=$(dir $(firstword $(MAKEFILE_LIST)))
makefile_name=$(notdir $(firstword $(MAKEFILE_LIST)))
script=$(makefile_dir)/script/

ifdef config
	include $(config)
else
	include $(makefile_dir)/config/config.txt
endif

HELP:
	@echo Description:对ASV后的数据进行物种注释
	@echo Program: tax.mk
	@echo Version: v1.0.0
	@echo Contactor: chengfangtu@genome.cn
	@echo tax_vsearch: 使用feature-classifier classify-consensus-vsearch对ASV数据进行物种注释
	@echo -e "\t" "make -f $(makefile_name) asv_rep= search_db= search_tax= tax_qza= cpu= tax_blast_qza= tax_maxreject= tax_maxaccept=  tax_identity= config= tax_vsearch"
	@echo 参数说明：
	@echo -e "\t" "输入"
	@echo -e "\t" "config: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/config/config.txt "
	@echo -e "\t" "asv_rep: [文件|必需] ASV表达文件，为asv.mk的Denoise的输出"
	@echo -e "\t" "search_db: [文件|必需] 物种数据库，qiime2建库的-seqs.qza文件"
	@echo -e "\t" "search_tax: [文件|必需] 物种数据库,qiime2建库的-tax.qza文件"
	@echo -e "\t" "参数"
	@echo -e "\t" "tax_maxreject: [字符串|可选] 最大拒绝数，默认为100"
	@echo -e "\t" "tax_maxaccept: [字符串|可选] 每个asv序列匹配上的hits最大保留数，默认为100"
	@echo -e "\t" "tax_identity: [字符串|可选] query和hit的最小相似度(0，1]，默认为0.97"
	@echo -e "\t" "输出"
	@echo -e "\t" "tax_qza: [字符串|必需] 物种注释输出文件，qza格式"
	@echo -e "\t" "tax_blast_qza: [字符串|必需] 物种注释blast输出文件，qza格式"

	@echo tax_stat: 对物种注释后的数据进行转化和统计
	@echo -e "\t" "make -f $(makefile_name) tax_qza= asv_freq= asv_rep= outdir= config= tax_stat"
	@echo 参数说明：
	@echo -e "\t" "输入"
	@echo -e "\t" "config: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/config/config.txt "
	@echo -e "\t" "tax_qza: [文件|必需] 物种注释输出文件，qza格式"
	@echo -e "\t" "asv_freq: [文件|必需] ASV频率输出文件，qza格式"
	@echo -e "\t" "asv_rep: [文件|必需] ASV表达输出文件，qza格式"
	@echo -e "\t" "输出"
	@echo -e "\t" "outdir: [字符串|可选]数据路径，数据路径创建tax_export和merge_qzv_export文件，在merge_qzv_export/metadata.tsv 文件中输出各个样本的ASV以及物种丰度"

tax_maxreject=100
tax_maxaccept=100
tax_identity=0.97
tax_vsearch:
	echo "############### tax_vsearch start at `date` ###############"
	mkdir -p $(dir $(firstword $(tax_qza)))
	source $(conda_activate) $(qiime2_env) && $(QIIME2) feature-classifier classify-consensus-vsearch --i-query $(asv_seq) \
	--o-classification $(tax_qza) \
	--o-search-results $(tax_blast_qza) \
	--i-reference-reads $(search_db) \
	--i-reference-taxonomy $(search_tax) \
	--p-threads $(cpu) \
	--p-maxrejects $(tax_maxreject) \
	--p-maxaccepts $(tax_maxaccept) \
	--p-perc-identity $(tax_identity) \
	--p-top-hits-only
	echo "############### tax_vsearch end at `date` ###############"


tax_stat:
	echo "############### tax_stat start at `date` ###############"
	mkdir -p $(outdir)
	$(QIIME2) tools export --input-path $(tax_qza) --output-path $(outdir)/tax_export
	$(QIIME2) feature-table transpose --i-table $(asv_freq) ----o-transposed-feature-table $(outdir)/transposed_asv.qza
	$(QIIME2) metadata tabulate --m-input-file $(asv_rep) --m-input-file $(tax_qza) --m-input-file $(outdir)/transposed_asv.qza --o-visualization $(outdir)/merge.qzv
	$(QIIME2) tools export --input-path $(outdir)/merge.qzv --output-path $(outdir)/merge_qzv_export
	echo "############### tax_stat end at `date` ###############"

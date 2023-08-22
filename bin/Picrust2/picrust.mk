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
	@echo prepare_picrust2: 准备Picrust2所需的输入文件
	@echo -e "\t" "make -f $(makefile_name) tax_tsv= outdir= config= prepare_picrust2"
	@echo 参数说明：
	@echo -e "\t" "输入"
	@echo -e "\t" "config: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/config/config.txt "
	@echo -e "\t" "tax_tsv: [文件|必需] ASV表格文件"
	@echo -e "\t" "输出"
	@echo -e "\t" "outdir: [字符串|必需] 输出目录，输出目录下会生成biom-taxonomy_vsearch.tsv,feature-table-tax_vsearch.biom-用于pircrust分析"
	@echo -e "\t" "out_biom: [字符串|必需] biom输出文件路径,"

	@echo Picrust2: 进行Picrust2分析
	@echo -e "\t" "make -f $(makefile_name) asv_fa= vsearch_biom= outdir= trait= cpu= config= Picrust2"
	@echo 参数说明：
	@echo -e "\t" "输入"
	@echo -e "\t" "config: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/config/config.txt "
	@echo -e "\t" "asv_fa: [文件|必需] 所有ASV序列的fa文件"
	@echo -e "\t" "vsearch_biom: [文件|必需] 物种注释后的文件转化为biom格式，为prepare_picrust2的输出"
	@echo -e "\t" "参数"
	@echo -e "\t" "trait: [字符串|可选] 做哪些分析，默认做EC,KO"
	@echo -e "\t" "cpu: [字符串|可选] 运行CPU数量，默认10"
	@echo -e "\t" "输出"
	@echo -e "\t" "outdir: [字符串|必需] 结果输出路径"

prepare_picrust2:
	echo "############### prepare_picrust2 start at `date` ###############"
	mkdir -p $(outdir)
	sed 's/Feature ID/#OTUID/' $(tax_tsv) | sed 's/Taxon/taxonomy/' | sed 's/Consensus/confidence/' > $(outdir)/biom-taxonomy_vsearch.tsv
	${QIIME2_DIR}/biom add-metadata -i $(outdir)/asv_freq/feature-table.biom \
	-o $(out_biom) \
	--observation-metadata-fp $(outdir)/biom-taxonomy_vsearch.tsv \
	--sc-separated taxonomy
	echo "############### prepare_picrust2 end at `date` ###############"

trait=EC,KO
cpu=10
Picrust2:
	echo "############### Picrust2 start at `date` ###############"
	mkdir -p $(outdir)
	source $(conda_activate) $(picrust_env) && picrust2_pipeline.py -s $(asv_fa) -i $(vsearch_biom) \
	-o $(outdir) \
	--in_traits $(trait) \
	--verbose -p $(cpu)
	echo "############### Picrust2 end at `date` ###############"
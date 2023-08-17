
##### cat makefile 
BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
file=$(abspath $(firstword $(MAKEFILE_LIST)))
script=$(BIN)/script/

ifdef config
	include $(config)
else 
	include $(BIN)/config/config.txt
endif

HELP:
	@echo  -e "\nUsage:"
	@echo Description: 进行alpha多样性分析（Alpha_vegan），以及指标差异boxplot图（Alpha_boxplot）
	@echo Program: mk_alpha
	@echo Version: v1.0.0
	@echo Contactor: chengfangtu@genome.cn
	@echo Alpha_vegan
	@echo -e "\t" "make -f $(makefile_name) merge_file= outdir= sample_list= software= Alpha_vegan"
	@echo 参数说明：
	@echo -e "\t" "software: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/software/software.txt "
	@echo -e "\t" "merge_file: [文件|必需]  输入文件，物种丰度文件，例如：merge.qiime.xls、otu.xls"
	@echo -e "\t" "outdir: [路径|必需]  分析结果输出路径 "
	@echo -e "\t" "sample_list: [文件|必需]  样本列表"
	@echo -e "\t" "make -f $(makefile_name) infile= outdir= outfile= software= Alpha_boxplot"
	@echo Alpha_boxplot
	@echo 参数说明：
	@echo -e "\t" "software: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/software/software.txt "
	@echo -e "\t" "infile: [文件|必需] 带有分组信息的alpha多样性指标表，即Alpha_vegan的输出文件"
	@echo -e "\t" "label: [字符|必需] alpha多样性指标名称，与infile中的列名一致，指定哪列做哪列 "
	@echo -e "\t" "outdir: [路径|必需]  分析结果输出路径 "
	@echo -e "\t" "prefix: [文件|必需]  输出文件前缀"
	@echo  -e "\nUsage:"
	@echo Description: 绘制α多样性曲线（rank：等级丰度曲线；rarefaction：稀释性曲线；accumulation：物种累积曲线）
	@echo Program: mk_alpha
	@echo Version: v1.0.0
	@echo Contactor: yangzhang@genome.cn
	@echo -e "\t" "make -f $(makefile_name) infile= outdir= outfile= software= rank"
	@echo -e "\t" "make -f $(makefile_name) infile= outdir= outfile= software= rarefaction"
	@echo -e "\t" "make -f $(makefile_name) infile= outdir= outfile= software= accumulation"
	@echo 参数说明：
	@echo -e "\t" "software: [文件|可选]  模块配置文件，和软件相关参数，默认为$(makefile_dir)/software/software.txt "
	@echo -e "\t" "infile: [文件|必需]  输入文件，物种丰度文件，例如：merge.qiime.xls、otu.xls"
	@echo -e "\t" "outdir: [路径|必需]  分析结果输出路径 "
	@echo -e "\t" "outfile: [文件|必需]  分析结果文件名 allsample.rank.curve.pdf; allsample.rarefaction.curve.pdf;allsample.accumulation.curve.pdf"



Alpha_vegan:
	@echo "===================== Run Alpha_vegan Begin at `date` ===================== "
	[ -d $(outdir) ] && rm -r $(outdir) || echo "ok"
	mkdir -p ${outdir}
	export OPENBLAS_NUM_THREADS=2 && ${QIIME2}/Rscript ${BIN}/script/alpha_diversity.R ${merge_file} ${outdir}/alpha_vegan.tmp.xls
	if [ -e ${outdir}/alpha_vegan.tmp.xls ] ;\
		then \
		sed '1cSample\tChao1\tACE\tObserved_species\tPielou\tShannon\tSimpson' ${outdir}/alpha_vegan.tmp.xls >${outdir}/alpha_vegan_out.xls ;\
		$(CSVTK) -t join ${outdir}/alpha_vegan_out.xls $(sample_list) > ${outdir}/alpha_vegan_boxplot.xls ;\
	else \
		echo "该项目不做alpha多样性分析" ;\
	fi
	@echo "===================== Run Alpha_vegan End at `date` ===================== "

Alpha_boxplot:
	@echo "===================== Run Alpha_boxplot Begin at `date` ===================== "
	if [ -e ${infile} ] ;\
		then \
			mkdir -p $(outdir) ;\
			$(PYTHON3) $(BIN)/script/de_boxplot.py -i $(infile) -o $(outdir)/$(prefix).pdf -l $(label) ;\
			$(CONVERT) $(outdir)/$(prefix).pdf $(outdir)/$(prefix).png ;\
	else \
		echo "输入文件不存在，不做差异分析" ;\
	fi
	@echo "===================== Run Alpha_boxplot End at `date` ===================== "


.PHONY:rank
rank:
	@echo "===================== Run rank curve Begin at `date` ===================== "
	if [ -e ${infile} ] ;\
		then \
		mkdir -p $(outdir)/ ;\
		$(Rscript) $(script)/rank.r -i $(infile) -o $(outdir)/$(outfile) -s $(script) ;\
		cd $(outdir) && for i in `ls *.pdf`; do $(CONVERT) $$i `basename $$i .pdf`.png ;done ;\
	else \
		echo "输入文件不存在，不绘图" ;\
	fi
	@echo "===================== Run rank curve End at `date` ===================== "

.PHONY:rarefaction
rarefaction:
	@echo "===================== Run rarefaction curve Begin at `date` ===================== "
	if [ -e ${infile} ] ;\
		then \
		mkdir -p $(outdir) ;\
		$(Rscript) $(script)/rarefaction.r -i $(infile) -o $(outdir)/$(outfile) ;\
		cd $(outdir) && for i in `ls *.pdf`; do $(CONVERT) $$i `basename $$i .pdf`.png ;done ;\
	else \
		echo "输入文件不存在，不绘图" ;\
	fi
	@echo "===================== Run rarefaction curve End at `date` ===================== "

.PHONY:accumulation
accumulation:
	@echo "===================== Run accumulation curve Begin at `date` ===================== "
	if [ -e ${infile} ] ;\
		then \
		mkdir -p $(outdir) ;\
		$(Rscript) $(script)/accumulation.r -i $(infile) -o $(outdir)/$(outfile) ;\
		cd $(outdir) && for i in `ls *.pdf`; do $(CONVERT) $$i `basename $$i .pdf`.png ;done ;\
	else \
		echo "输入文件不存在，不绘图" ;\
	fi
	@echo "===================== Run accumulation curve End at `date` ===================== "

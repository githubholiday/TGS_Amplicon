##### cat makefile 
BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
file=$(abspath $(firstword $(MAKEFILE_LIST)))


ifdef config
	include $(config)
else 
	include $(BIN)/config/config.txt
endif
Help:
	@echo Info:
	@echo -e "\t" Author: chengfangtu
	@echo -e "\t" Version: v1.0.0
	@echo -e "\t" Date: 2023-5-11
	@echo -e "Description:"
	@echo -e "\t"该脚本用于物种多样性的Beta分析的内容
	@echo target:
	@echo -e "\t" Beta_qiime: 使用qiime计算beta多样性
	@echo -e "\t" NMDS:做NMDS分析
	@echo -e "\t" PCA:PCA分析
	@echo -e "\t" PCoA:PCoA分析
	@echo -e "\n" Usage-Beta_qiime:
	@echo -e "\t" make -f $(file) config= qza_file= method= outdir= Beta_qiime
	@echo -e "\t"参数说明:
	@echo -e "\t" "config: [文件|可选]模块配置文件，和软件相关参数，默认为$(BIN)/config/config.txt "
	@echo -e "\t" "qza_file: [文件|必需]所有样本物种丰度qza文件"
	@echo -e "\t" "method: [字符|必需]beta距离计算方法,可选[braycurtis,jaccard]"
	@echo -e "\t" "outdir: [目录|必需]输出目录，输出目录下输出 beta_qiime_${method}.xls,beta_qiime_${method}.heatmap.pdf,beta_qiime_${method}.heatmap.png"
	@echo -e "\n"Usage-NMDS:
	@echo -e "\t" make -f $(file) config= merge_file= cmp= outdir= NMDS
	@echo -e "\t"参数说明:
	@echo -e "\t" "config: [文件|可选]模块配置文件，和软件相关参数，默认为$(BIN)/config/config.txt "
	@echo -e "\t" "merge_file: [文件|必需]所有样本物种丰度合并文件"
	@echo -e "\t" "method: [文件|必需]计算方法"
	@echo -e "\t" "prefix: [文件|必需]输出文件前缀，prefix.pdf,prefix.png"
	@echo -e "\t" "cmp: [字符|必需]样本和组对应关系文件,第一列为样本,第二列为组名"
	@echo -e "\t" "outdir: [目录|必需]输出目录,输出目录下输出NMDS.pdf,NMDS.png"
	@echo -e "\n"Usage-PCA:
	@echo -e "\t" make -f $(file) config= sample_format_file= sample_rate_file= cmp= outdir= PCA
	@echo -e "\t"参数说明:
	@echo -e "\t" "config: [文件|可选]模块配置文件，和软件相关参数，默认为$(BIN)/config/config.txt "
	@echo -e "\t" "sample_format_file: [文件|必需]样本的物种丰度文件"
	@echo -e "\t" "sample_rate_file: [文件|必需]样本物种丰度的比例文件"
	@echo -e "\t" "cmp: [字符|必需]样本和组对应关系文件,第一列为样本,第二列为组名"
	@echo -e "\t" "outdir: [目录|必需]输出目录,输出目录下输出PCA.3d.p*,PCA.p*"
	@echo -e "\n"Usage-PCoA:
	@echo -e "\t" make -f $(file) config= infile= method= cmp= outdir= pdf_name= table_name= axis_name= PCA
	@echo -e "\t"参数说明:
	@echo -e "\t" "config: [文件|可选]模块配置文件，和软件相关参数，默认为$(BIN)/config/config.txt "
	@echo -e "\t" "infile: [文件|必需]所有样本物种丰度合并文件"
	@echo -e "\t" "method: [文件|必需]beta距离计算方法,可选[bray,jaccard]"
	@echo -e "\t" "cmp: [字符|必需]样本和组对应关系文件,第一列为样本,第二列为组名"
	@echo -e "\t" "outdir: [目录|必需]输出目录,输出目录下输出PCA.3d.p*,PCA.p*"
	@echo -e "\t" "pdf_name: [字符|必需]输出的图片文件名"
	@echo -e "\t" "table_name: [字符|必需]输出的样本文件名"
	@echo -e "\t" "axis_name: [字符|必需]输出的坐标轴说明文件名"


Beta_qiime:
	@echo "===================== Run Beta_qiime Begin at `date` ===================== "
	mkdir -p ${outdir}/tmp/$(method)
	${QIIME2} diversity beta --i-table ${qza_file} --p-metric ${method} --o-distance-matrix ${outdir}/beta_qiime_${method}.qza
	${QIIME2} tools export --input-path ${outdir}/beta_qiime_${method}.qza --output-path ${outdir}/tmp/$(method)
	${PYTHON3} ${BIN}/script/retain_float.py -i ${outdir}/tmp/$(method)/distance-matrix.tsv -o ${outdir}/beta_qiime_${method}.xls
	${QIIME2}/Rscript ${BIN}/script/draw_heat.r ${outdir}/tmp/$(method)/distance-matrix.tsv ${outdir}/beta_qiime_${method}.heatmap.pdf
	${CONVERT} ${outdir}/beta_qiime_${method}.heatmap.pdf ${outdir}/beta_qiime_${method}.heatmap.png
	@echo "===================== Run Beta_qiime End at `date` ===================== "

NMDS:
	@echo "===================== Run NMDS Begin at `date` ===================== "
	mkdir -p ${outdir}
	${QIIME2_DIR}/Rscript ${BIN}/script/nmds.r ${merge_file} ${cmp} ${outdir}/$(prefix).pdf $(method)
	${CONVERT} ${outdir}/$(prefix).pdf ${outdir}/$(prefix).png
	@echo "===================== Run NMDS End at `date` ===================== "


PCA_old:
	@echo "===================== Run PCA Begin at `date` ===================== "
	mkdir -p ${outdir}
	#${PYTHON3} ${BIN}/script/braken_report_format.py -i ${sample_format_file} -e ${sample_rate_file} -r ${outdir}/merge.raw.richness.xls -c ${cmp}
	#cat ${outdir}/merge.raw.richness.xls|sed '2d'|awk -F "|" '{print $$NF}' >${outdir}/merge.richness.xls
	${PYTHON3} ${BIN}/script/change_format.py ${outdir}/merge.richness.xls ${outdir}/merge.richness.tmp.xls
	cat ${cmp}|sed '1iname\tgroup'|sed '2d' >${outdir}/cmp.list
	${Rscript} ${BIN}/script/pca.r ${outdir}/merge.richness.tmp.xls ${outdir}/cmp.list ${outdir}/ FALSE
	${CONVERT} ${outdir}/PCA_analysis/PCA.3d.pdf ${outdir}/PCA_analysis/PCA.3d.png
	${CONVERT} ${outdir}/PCA_analysis/PCA_individual_dim1_dim2.pdf ${outdir}/PCA.png
	mv ${outdir}/PCA_analysis/PCA_individual_dim1_dim2.pdf ${outdir}/PCA.pdf
	${CONVERT} ${outdir}/PCA_analysis/PCA_variable_dim1_dim2.pdf ${outdir}/PCA_analysis/PCA_variable_dim1_dim2.png
	@echo "===================== Run PCA End at `date` ===================== "

PCA:
	@echo "===================== Run PCA Begin at `date` ===================== "
	mkdir -p ${outdir}
	cat ${cmp}|cut -f 1,2 |sed '1iname\tgroup'|sed '2d' >${outdir}/cmp.list
	${Rscript} ${BIN}/script/pca.r ${infile} ${outdir}/cmp.list ${outdir}/ FALSE
	${CONVERT} ${outdir}/PCA_analysis/PCA.3d.pdf ${outdir}/PCA_analysis/PCA.3d.png
	mv ${outdir}/PCA_analysis/PCA_individual_dim1_dim2.pdf ${outdir}/PCA.pdf
	${CONVERT} ${outdir}/PCA.pdf ${outdir}/PCA.png
	${CONVERT} ${outdir}/PCA_analysis/PCA_variable_dim1_dim2.pdf ${outdir}/PCA_analysis/PCA_variable_dim1_dim2.png
	@echo "===================== Run PCA End at `date` ===================== "

PCoA:
	@echo "===================== Run PCoA Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(Rscript) ${BIN}/script/PCoA.r -i $(infile) -c $(cmp) -m $(method) -p $(outdir)/$(pdf_name) -o $(outdir)/$(table_name) -O $(outdir)/$(axis_table)
	cd $(outdir) && for i in `ls *.pdf`; do $(CONVERT) $$i `basename $$i .pdf`.png ;done
	@echo "===================== Run PCoA End at `date` ===================== "


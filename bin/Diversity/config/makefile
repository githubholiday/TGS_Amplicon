##### cat makefile 
BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
file=$(abspath $(firstword $(MAKEFILE_LIST)))
include $(config)
###默认参数
LDA?=2

Help:
	@echo Description:
	@echo -e "\t" 该脚本用于物种多样性分析
	@echo -e "\t" Author "\t": liaorui
	@echo target:
	@echo -e "\t" Alpha_qiime "\t": 使用qiime计算alpha多样性
	@echo -e "\t" Alpha_phyloseq "\t": 使用phyloseq计算alpha多样性
	@echo -e "\t" Alpha_vegan "\t": 使用vegan计算alpha多样性
	@echo -e "\t" Beta_qiime "\t": 使用qiime计算beta多样性
	@echo -e "\t" Diff_lefse "\t": 使用lefse进行差异分析
	@echo Usage:
	@echo -e "\t" make -f ${file} sample= outdir= kraken_report= Alpha_qiime
	@echo -e "\t" make -f ${file} sample=M31,M32,M33,M34,M35,M36 outdir=${BIN}/output kraken_report=/annoroad/data1/bioinfo/PROJECT/RD/Cooperation/RD_Group/lihuayun/NGS_Meta_Test/NGS_Meta_Test3/ Alpha_qiime
	@echo -e "\t" make -f ${file} sample= outdir= kraken_report= Alpha_phyloseq
	@echo -e "\t" make -f ${file} kraken_report= outdir= Alpha_vegan
	@echo -e "\t" make -f ${file} sample= outdir= kraken_report= Beta_qiime
	@echo -e "\t" make -f ${file} outdir= kraken_report= sample= cmp= LDA= Diff_lefse
	@echo Parameters:
	@echo -e "\t" sample "\t": 样本名称
	@echo -e "\t" outdir "\t": 输出目录路径
	@echo -e "\t" kraken_report "\t": kraken结果目录
	@echo -e "\t" count "\t": 统计的count文件
	
qiime_format:
	mkdir -p ${outdir}
	${PYTHON3} ${BIN}/script/braken_report_format.py -i ${infile} -o ${outdir}/merge.qiime.xls
	${QIIME2}/biom convert -i ${outdir}/merge.qiime.xls -o ${outdir}/merge.biom  --to-hdf5 --table-type="OTU table"
	${QIIME2}/qiime tools import --input-path ${outdir}/merge.biom --type 'FeatureTable[Frequency]' --input-format BIOMV210Format --output-path ${outdir}/all_qiime.qza

Alpha_vegan:
	echo Alpha_vegan start at `date`
	mkdir -p ${outdir}
	${QIIME2}/Rscript ${BIN}/script/alpha_diversity.R ${merge_file} ${outdir}/alpha_vegan.tmp.xls
	sed '1cSample\tChao1\tACE\tObserved_species\tPielou\tShannon\tSimpson' ${outdir}/alpha_vegan.tmp.xls >${outdir}/alpha_vegan_out.xls
	$(CSVTK) -t join ${outdir}/alpha_vegan_out.xls $(sample_list) > ${outdir}/alpha_vegan_boxplot.xls
	echo Alpha_vegan end at `date`

Alpha_boxplot:
	echo Alpha_boxplot start at `date`
	mkdir $(outdir)
	$(PYTHON3) $(BIN)/script/de_boxplot.py -i $(infile) -o $(outdir)/$(prefix).pdf -l $(label)
	$(CONVERT) $(outdir)/$(prefix).pdf $(outdir)/$(prefix).png
	echo Alpha_boxplot end at `date`

Beta_qiime:
	echo Beta_qiime $(method) start at `date`
	mkdir -p ${outdir}/tmp/$(method)
	${QIIME2}/qiime diversity beta --i-table ${qza_file} --p-metric ${method} --o-distance-matrix ${outdir}/beta_qiime_${method}.qza
	${QIIME2}/qiime tools export --input-path ${outdir}/beta_qiime_${method}.qza --output-path ${outdir}/tmp/$(method)
	${PYTHON3} ${BIN}/script/retain_float.py -i ${outdir}/tmp/$(method)/distance-matrix.tsv -o ${outdir}/beta_qiime_${method}.xls
	${QIIME2}/Rscript ${BIN}/script/draw_heat.r ${outdir}/tmp/$(method)/distance-matrix.tsv ${outdir}/beta_qiime_${method}.heatmap.pdf
	${CONVERT} ${outdir}/beta_qiime_${method}.heatmap.pdf ${outdir}/beta_qiime_${method}.heatmap.png
	echo Beta_qiime $(method) end at `date`

NMDS:
	echo Beta_qiime NMDS  start at `date`
	[ -s ${outdir} ] || mkdir -p ${outdir}
	${QIIME2}/Rscript ${BIN}/script/nmds.r ${merge_file} ${cmp} ${outdir}/NMDS.pdf
	${CONVERT} ${outdir}/NMDS.pdf ${outdir}/NMDS.png
	echo Beta_qiime NMDS  end at `date`


PCA:
	mkdir -p ${outdir}
	${PYTHON3} ${BIN}/script/braken_report_format.py -i ${sample_format_file} -e ${sample_rate_file} -r ${outdir}/merge.raw.richness.xls -c ${cmp}
	cat ${outdir}/merge.raw.richness.xls|sed '2d'|awk -F "|" '{print $$NF}' >${outdir}/merge.richness.xls
	${PYTHON3} ${BIN}/script/change_format.py ${outdir}/merge.richness.xls ${outdir}/merge.richness.tmp.xls
	cat ${cmp}|sed '1iname\tgroup'|sed '2d' >${outdir}/cmp.list
	${Rscript} ${BIN}/script/pca.r ${outdir}/merge.richness.tmp.xls ${outdir}/cmp.list ${outdir}/ FALSE
	${CONVERT} ${outdir}/PCA_analysis/PCA.3d.pdf ${outdir}/PCA_analysis/PCA.3d.png
	${CONVERT} ${outdir}/PCA_analysis/PCA_individual_dim1_dim2.pdf ${outdir}/PCA.png
	mv ${outdir}/PCA_analysis/PCA_individual_dim1_dim2.pdf ${outdir}/PCA.pdf
	${CONVERT} ${outdir}/PCA_analysis/PCA_variable_dim1_dim2.pdf ${outdir}/PCA_analysis/PCA_variable_dim1_dim2.png
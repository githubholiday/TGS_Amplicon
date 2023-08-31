BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
file=$(abspath $(firstword $(MAKEFILE_LIST)))

ifdef config
	include $(config)
else
	include $(BIN)/config/config.txt
endif

LDA=2
Diff_lefse:
	@echo "===================== Run Diff_lefse Begin at `date` ===================== "
	mkdir -p ${outdir}
	$(PYTHON3) $(BIN)/script/add_group.py -i $(infile) -o $(outdir)/diff.group.xls -s $(cmp)
	source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_format_input.py $(outdir)/diff.group.xls ${outdir}/merge.lefse.in -c 2 -u 1 -o 1000000
	source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_run.py ${outdir}/merge.lefse.in ${outdir}/merge.lefse.lda.res -l ${LDA} 
	source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_plot_res.py --format pdf ${outdir}/merge.lefse.lda.res ${outdir}/lefse.lda.pdf
	${CONVERT} ${outdir}/lefse.lda.pdf ${outdir}/lefse.lda.png
	source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_plot_features.py --format pdf -f diff --archive zip ${outdir}/merge.lefse.in ${outdir}/merge.lefse.lda.res ${outdir}/biomarkers.zip
	cat ${outdir}/merge.lefse.lda.res|grep -v '-'|awk -F "\t" '{if($$4>=${LDA})print $$0}' >${outdir}/merge.lefse.lda.significant.res
	source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_plot_cladogram.py --format pdf ${outdir}/merge.lefse.lda.significant.res ${outdir}/all_level_lefse_significant_cladogram.pdf
	${CONVERT} ${outdir}/all_level_lefse_significant_cladogram.pdf ${outdir}/all_level_lefse_significant_cladogram.png
	@echo "===================== Run Diff_lefse End at `date` ===================== "

add_group:
	@echo "===================== Run add group for lefse Begin at `date` ===================== "
	$(PYTHON3) $(BIN)/script/add_group.py -i $(infile)  -s $(sample_list) -o $(outdir)/diff.group.xls
	@echo "===================== Run add group for lefse End at `date` ===================== "

lefse_diff:
	@echo "===================== Run Diff_lefse Begin at `date` ===================== "
	if [ $(diff_on) == 'diff' ];\
		then \
		mkdir -p $(outdir) ;\
		$(PYTHON3) $(BIN)/script/add_group_select.py -i $(infile) -s $(sample_list) -o $(outdir)/$(cmp1)_$(cmp2).diff.group.xls -cmp $(cmp1) $(cmp2) ;\
		source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_format_input.py $(outdir)/$(cmp1)_$(cmp2).diff.group.xls ${outdir}/$(cmp1)_$(cmp2).merge.lefse.in -c 2 -u 1 -o 1000000 ;\
		source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_run.py ${outdir}/$(cmp1)_$(cmp2).merge.lefse.in ${outdir}/$(cmp1)_$(cmp2).merge.lefse.lda.res -l ${LDA}  ;\
		source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_plot_res.py --format pdf ${outdir}/$(cmp1)_$(cmp2).merge.lefse.lda.res ${outdir}/$(cmp1)_$(cmp2).lefse.lda.pdf ;\
		${CONVERT} ${outdir}/$(cmp1)_$(cmp2).lefse.lda.pdf ${outdir}/$(cmp1)_$(cmp2).lefse.lda.png ;\
		source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_plot_features.py --format pdf -f diff --archive zip ${outdir}/$(cmp1)_$(cmp2).merge.lefse.in ${outdir}/$(cmp1)_$(cmp2).merge.lefse.lda.res ${outdir}/biomarkers.zip --subcl_median n --subcl_mean y;\
		cat ${outdir}/$(cmp1)_$(cmp2).merge.lefse.lda.res|grep -v '-'|awk -F "\t" '{if($$4>=${LDA})print $$0}' >${outdir}/$(cmp1)_$(cmp2).merge.lefse.lda.significant.res ;\
		source ${lefse_conda} && ${LEFSE}/python3 ${LEFSE}/lefse_plot_cladogram.py --format pdf ${outdir}/$(cmp1)_$(cmp2).merge.lefse.lda.significant.res ${outdir}/$(cmp1)_$(cmp2).significant_cladogram.pdf ;\
		${CONVERT} ${outdir}/$(cmp1)_$(cmp2).significant_cladogram.pdf ${outdir}/$(cmp1)_$(cmp2).significant_cladogram.png ;\
	else\
		echo "this cmp do not analysis diff by lefse";\
	fi
	@echo "===================== Run Diff_lefse End at `date` ===================== "

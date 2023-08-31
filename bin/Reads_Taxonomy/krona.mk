BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
file=$(abspath $(firstword $(MAKEFILE_LIST)))

ifdef config
	include $(config)
else
	include $(BIN)/config/config.txt
endif
Help:
	@echo Description:
	@echo -e "\t" 该脚本使用krona绘制物种分布圈图
	@echo -e "\t" Author "\t": liaorui
	@echo target:
	@echo -e "\t" krona "\t": 使用krona绘制物种分布圈图
	@echo Usage:
	@echo -e "\t" make -f $(file) infile= outdir= prefix= Krona
	@echo Parameters:
	@echo -e "\t" config "\t": 配置文件,软件等配置文件，默认为 config/config.txt文件
	@echo -e "\t" asv_freq "\t": asv_freq结果
	@echo -e "\t" taxonomy "\t": Tax步骤的taxonomy.vsearch.qza文件
	@echo -e "\t" outdir "\t": 输出文件夹，输出krona_html

.PHONY:krona
krona:
	@echo "===================== Run Krona Begin at `date` ===================== "
	mkdir -p $(outdir)
	source $(conda_activate) $(qiime2_env)&& $(QIIME2) krona collapse-and-plot --i-table $(asv_freq) --i-taxonomy $(taxonomy) --o-krona-plot $(outdir)/krona.qzv
	$(QIIME2) tools export --input-path $(outdir)/krona.qzv --output-path $(outdir)/krona_html
	@echo "===================== Run Krona End at `date` ===================== "


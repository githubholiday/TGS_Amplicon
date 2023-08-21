BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)
file=$(abspath $(firstword $(MAKEFILE_LIST)))
threads?=10
top?=10
kmer?=100

alignment_dir=$(outdir)/assemble/$(sample)

Help:
	@echo Description:
	@echo -e "\t" 该脚本用于物种注释
	@echo -e "\t" Author "\t": liaorui
	@echo target:
	@echo -e "\t" kraken_bracken "\t": 使用braken和kraken进行注释
	@echo -e "\t" krona "\t": 使用krona绘制物种分布圈图
	@echo Usage:
	@echo -e "\t" make -f $(file) outdir= sample= cleandir= kraken_bracken
	@echo -e "\t" make -f $(file) outdir= sample= krona
	@echo Parameters:
	@echo -e "\t" outdir "\t": 输出文件夹
	@echo -e "\t" sample "\t": 样本名称
	@echo -e "\t" cleandir "\t": clean数据路径

OTU_Stat:
	@echo "===================== Run OTU_Stat Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/taxnomy_stat.py -i $(infile) -o $(outdir)/stat.xls -to $(outdir)/taxnomy.stat.xls
	$(PYTHON3) $(BIN)/script/taxnomy_rate.py -i $(stat_file) -s $(outdir)/stat.xls -o $(outdir)/taxnomy.rate.xls
	cat $(infile) | cut -f 1,3- |sed '2d'> $(outdir)/otu.table.xls
	$(PYTHON3) $(BIN)/script/OTU_num_plot.py -i $(outdir)/stat.xls -o $(outdir)/otu_num.pdf
	$(CONVERT) $(outdir)/otu_num.pdf $(outdir)/otu_num.png
	@echo "===================== Run OTU_Stat End at `date` ===================== "


Sample_Format:
	@echo "===================== Run Sample_Format Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/taxnomy_format.py -i $(infile) -o $(outdir)
	@echo "===================== Run Sample_Format End at `date` ===================== "


Group_Format:
	@echo "===================== Run Group_Format Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/group_format.py -i $(indir) -g $(group_file) -o $(outdir)
	@echo "===================== Run Group_Format End at `date` ===================== "


Draw_rich:
	@echo "===================== Run Draw_rich Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/get_top.py -i $(infile) -o $(outdir) -t $(top) -p richness
	$(PYTHON3) $(BIN)/script/generate_rich_plot_sh.py -i $(outdir)/*$(top)_top.xls -o $(outdir)/${top}_rich_plot.sh --Rscript $(QIIME2)/Rscript --convert $(CONVERT) -r $(BIN)/script/draw_richeness.r
	sh $(outdir)/${top}_rich_plot.sh
	@echo "===================== Run Draw_rich End at `date` ===================== "

Draw_heat:
	@echo "===================== Run Draw_heat Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/get_top.py -i $(infile) -o $(outdir) -t $(top) -p heatmap
	$(PYTHON3) $(BIN)/script/generate_heat_plot_sh.py -i $(outdir)/*$(top)_top.xls -o $(outdir)/${top}_heat_plot.sh --Rscript $(QIIME2)/Rscript --convert $(CONVERT) -r $(BIN)/script/draw_heat.r
	sh $(outdir)/${top}_heat_plot.sh
	@echo "===================== Run Draw_heat End at `date` ===================== "
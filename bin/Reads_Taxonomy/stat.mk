BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)
file=$(abspath $(firstword $(MAKEFILE_LIST)))
threads?=10
top?=10
kmer?=100

alignment_dir=$(outdir)/assemble/$(sample)

Help:
	@echo Description:
	@echo -e "\t" 该脚本用于物种注释后的统计和绘图
	@echo -e "\t" Author "\t": chengfangtu

	@echo OTU_Stat "\t": OTU数量统计
	@echo Usage:
	@echo -e "\t" make -f $(file) infile= outdir= stat_file= OTU_Stat
	@echo Parameters:
	@echo -e "\t" infile : 物种注释特征表，列分别为 ASV_id, 序列，物种，一致性，样本名。该文件为tax_vsearch的输出文件
	@echo -e "\t" stat_file:样本过滤表，列分别为样本名，原始数据，有效数据，有效数据比例，平均长度。为cutadapt的统计结果
	@echo -e "\t" outdir: 输出文件夹，该文件夹下分别输出：stat.xls(各个样本的ASV数量以及read数量)；otu.table.xls（将Infile中的序列去除后的文件）；taxnomy.rate.xls-注释比例统计文件，taxnomy.stat.xls-各物种注释丰度统计文件；otu_num.p*-各个样本ASV数量柱形图

	@echo Sample_Format "\t": 样本注释文件格式化
	@echo Usage:
	@echo -e "\t" make -f $(file) infile= outdir= Sample_Format
	@echo Parameters:
	@echo -e "\t" infile "\t": 物种注释特征表，列分别为 ASV_id, 序列，物种，一致性，样本名。该文件为tax_vsearch的输出文件
	@echo -e "\t" outdir "\t": 输出文件夹，输出文件为：*.format.xls(单样本物种注释丰度文件)，*.species.rate.xls:各样本不同物种占比统计文件

	@echo Group_Format "\t": 样本分组文件格式化
	@echo Usage:
	@echo -e "\t" make -f $(file) indir= group_file= outdir= Group_Format
	@echo Parameters:
	@echo -e "\t" indir "\t": 样本注释文件夹，该文件夹下为各个样本的物种注释文件，文件名为样本名
	@echo -e "\t" group_file "\t": 样本分组文件，第一列为组名，后面列为该组包含的样本名称
	@echo -e "\t" outdir "\t": 输出文件夹，输出文件为：*.format.xls(组物种注释丰度文件)

	@echo Draw_rich "\t": 绘制物种丰度柱形图
	@echo Usage:
	@echo -e "\t" make -f $(file) infile= outdir= top= Draw_rich
	@echo Parameters:
	@echo -e "\t" infile "\t": 各个样本或比较组的format.xls文件
	@echo -e "\t" outdir "\t": 输出文件夹，输出文件为：richness_1_division_10_top.pdf(物种丰度柱形图)；richness_1_division_10_top.xls:不同物种层级的top物种丰度文件
	@echo -e "\t" top:选择前top物种绘图,选取规则:选择每个样本/组中的前top物种，将这些物种合并后作为最终的top物种，所以最终结果可能超过top物种。一般选择前10

	@echo Draw_heat "\t": 绘制物种注释热图
	@echo Usage:
	@echo -e "\t" make -f $(file) infile= outdir= top= Draw_heat
	@echo Parameters:
	@echo -e "\t" infile "\t": 各个样本或比较组的format.xls文件
	@echo -e "\t" outdir "\t": 输出文件夹，输出文件为：heatmap_1_division_35_top.pdf(物种注释热图)；*heatmap_1_division_35_top.xls:不同物种层级的top物种丰度文件
	@echo -e "\t" top:选择前top物种绘图,选取规则:选择每个样本/组中的前top物种，将这些物种合并后作为最终的top物种，所以最终结果可能超过top物种。一般选择前35。
	@echo -e "\t"说明：如果样本/组少于2个，不绘制图，因为无法计算相关性

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
	$(PYTHON3) $(BIN)/script/generate_rich_plot_sh.py -i $(outdir)/*$(top)_top.xls -o $(outdir)/${top}_rich_plot.sh --Rscript $(QIIME2_Dir)/Rscript --convert $(CONVERT) -r $(BIN)/script/draw_richeness.r
	sh $(outdir)/${top}_rich_plot.sh
	@echo "===================== Run Draw_rich End at `date` ===================== "

Draw_heat:
	@echo "===================== Run Draw_heat Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/get_top.py -i $(infile) -o $(outdir) -t $(top) -p heatmap
	$(PYTHON3) $(BIN)/script/generate_heat_plot_sh.py -i $(outdir)/*$(top)_top.xls -o $(outdir)/${top}_heat_plot.sh --Rscript $(QIIME2_Dir)/Rscript --convert $(CONVERT) -r $(BIN)/script/draw_heat.r
	sh $(outdir)/${top}_heat_plot.sh
	@echo "===================== Run Draw_heat End at `date` ===================== "
BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)
file=$(abspath $(firstword $(MAKEFILE_LIST)))


Help:
	@echo Description:
	@echo -e "\t" 该脚本用于funguild分析以及funguild的统计绘图
	@echo -e "\t" Author "\t": chengfangtu"
	@echo -e "\n*****funguild: ITs功能注释"
	@echo -e "\t" make -f $(file) config= infile= prefix= outdir= cog_plot
	@echo -e "\t config: [输入|必需]软件和数据库配置文件，默认为 config/config.txt"
	@echo -e "\t tax: [输入|必需] 物种注释文件"
	@echo -e "\t outdir: [输出|必需]输出路径,输出结果为tax.taxa.guilds.txt"

funguild:
	@echo "===================== Run funguild Begin at `date` ===================== "
	mkdir -p $(outdir)
	cp $(tax) $(outdir)/tax.txt
	cd $(outdir) &&  $(PYTHON3) $(FUNGUILD)/FUNGuild.py taxa -otu $(outdir)/tax.txt -format tsv -column Taxon -classifier unite
	cd $(outdir) &&  $(PYTHON3) $(FUNGUILD)/FUNGuild.py guild -taxa $(outdir)/tax.taxa.txt
	@echo "===================== Run funguild End at `date` ===================== "

funguild_stat:
	@echo "===================== Run funguild stat Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/guild_stat.py -g $(infile) -o $(outdir)/$(prefix).xls
	$(Rscript) $(BIN)/script/draw_guild.r $(outdir)/$(prefix).xls $(outdir)/$(prefix).pdf
	[ -f $(outdir)/$(prefix).pdf ] && convert -density 300 $(outdir)/$(prefix).pdf $(outdir)/$(prefix).png || echo no $(outdir)/$(prefix).pdf
	@echo "===================== Run funguild stat End at `date` ===================== "

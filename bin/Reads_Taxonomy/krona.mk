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
	@echo -e "\t" infile "\t": 输入文件,每一列为物种名称,最后一列为物种的reads数
	@echo -e "\t" prefix "\t": 输入文件前缀
	@echo -e "\t" outdir "\t": 输出文件夹,输出prefix.krona.xls和prefix.krona.html

Krona:
	@echo "===================== Run Krona Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/krona_format.py -i $(infile) -o $(outdir)/$(prefix).krona.xls
	$(ktImportText) $(outdir)/$(prefix).krona.xls -o $(outdir)/$(prefix).krona.html
	@echo "===================== Run Krona End at `date` ===================== "


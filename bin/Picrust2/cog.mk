BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)
file=$(abspath $(firstword $(MAKEFILE_LIST)))


Help:
	@echo Description:
	@echo -e "\t" 该脚本用于cog注释结果统计和绘图
	@echo -e "\t" Author "\t": chengfangtu
	@echo target:
	@echo -e "\t" cog_anno "\t": 基于picrust2的结果增加COG的注释信息，并按照样本统计各个COG类型注释到数量
	@echo -e "\t" cog_plot "\t": 绘制COG分类统计图
	@echo -e "\n*****cog_anno使用说明:"
	@echo -e "\t" make -f $(file) config= cog_in= cog= cog_fun= outdir= cog_anno
	@echo -e "\t config: [输入|必需]软件和数据库配置文件，默认为 config/config.txt"
	@echo -e "\t cog_in: [输入|必需] COG数据库的COG和大类的对应关系文件，默认为 /annoroad/data1/bioinfo/PROJECT/Commercial/Cooperation/FTP/Database/COG/current/data/cog.txt"
	@echo -e "\t cog_fun: [输入|必需]COG数据库的大类的对应关系文件，默认为 /annoroad/data1/bioinfo/PROJECT/Commercial/Cooperation/FTP/Database/COG/current/data/fun_format.txt"
	@echo -e "\t outdir: [输出|必需]输出路径，输出路径下创建Sample目录，并在该目录下输出每个样本的COG大类统计文件"
	@echo -e "\n*****cog_plot 使用说明:"
	@echo -e "\t" make -f $(file) config= infile= prefix= outdir= cog_plot
	@echo -e "\t config: [输入|必需]软件和数据库配置文件，默认为 config/config.txt"
	@echo -e "\t infile: [输入|必需] 每个样本的COG大类统计文件，第一列为大类编号如A，第二列为大类名称，第三列为注释到的数量，如果没注释上，即为0，需要保留没注释上的信息，以保证所有图都是一样的"
	@echo -e "\t prefix: [输出|必需]输出文件（图片）的前缀"
	@echo -e "\t outdir: [输出|必需]输出路径"

cog_anno:
	@echo "===================== Run cog_anno Begin at `date` ===================== "
	[ -d $(outdir)/Sample ] && rm -rf $(outdir)/Sample || echo ok
	mkdir -p $(outdir)
	mkdir -p $(outdir)/Sample
	$(CSVTK) -t join $(cog_in) $(cog) > $(outdir)/cog.anno.csv
	$(PYTHON3) $(BIN)/script/cog_stat.py -a $(outdir)/cog.anno.csv -f $(cog_fun) -o $(outdir)/Sample
	$(CSVTK) -t join $(outdir)/Sample/*cog.stat.xls > $(outdir)/allsample.cog.stat.tmp.xls
	$(PYTHON3) $(BIN)/script/del_repeat_col.py -i $(outdir)/allsample.cog.stat.tmp.xls -o $(outdir)/allsample.cog.stat.xls -r function
	@echo "===================== Run cog_anno End at `date` ===================== "

cog_plot:
	@echo "===================== Run cog_plot Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(Rscript) $(BIN)/script/draw_cog.r $(infile) $(outdir)/$(prefix).pdf
	$(CONVERT) $(outdir)/$(prefix).pdf $(outdir)/$(prefix).png
	@echo "===================== Run cog_plot End at `date` ===================== "

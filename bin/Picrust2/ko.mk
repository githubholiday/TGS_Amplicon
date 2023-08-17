BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)
file=$(abspath $(firstword $(MAKEFILE_LIST)))


Help:
	@echo Description:
	@echo -e "\t" 计算pathway不同等级的数量，并绘制classI的分布图
	@echo -e "\t" Author "\t": chengfangtu
	@echo -e "\n*****pathway_stat 使用说明:"
	@echo -e "\t" make -f $(file) config= ko_in= cog= komap= map_pathway= outdir= pathway_stat
	@echo -e "\t config: [输入|必需]软件和数据库配置文件，默认为 config/config.txt"
	@echo -e "\t ko_in: [输入|必需] 样本的KO注释结果，picrust2软件的结果"
	@echo -e "\t komap: [输入|必需]KO和map的对应关系，默认为/annoroad/data1/bioinfo/PROJECT/Commercial/Cooperation/FTP/Database/KEGG/current/data/ko2map/ko2map.xls"
	@echo -e "\t map_pathway: [输入|必需]map和pathway不同层级的对应关系,默认为：/annoroad/data1/bioinfo/PROJECT/Commercial/Cooperation/FTP/Database/KEGG/20221108/data/map_pathway.list"
	@echo -e "\t outdir: [输出|必需]输出路径，输出路径下创建Sample目录，并在该目录下输出每个样本的map统计文件"

pathway_stat:
	@echo "===================== Run pathway stat Begin at `date` ===================== "
	[ -d $(outdir) ] && rm -rf $(outdir) || echo ok
	mkdir -p $(outdir)
	mkdir -p $(outdir)/Sample
	$(CSVTK) -t join $(ko_in) $(komap) > $(outdir)/pathway.anno.csv
	$(PYTHON3) $(BIN)/script/map_stat.py -a $(outdir)/pathway.anno.csv -m $(map_pathway) -o $(outdir)/Sample
	$(CSVTK) -t join $(outdir)/Sample/*classI.stat.xls > $(outdir)/allsample.pathway.I.stat.xls
	$(CSVTK) -t join $(outdir)/Sample/*classII.stat.xls > $(outdir)/allsample.pathway.II.stat.tmp.xls
	$(CSVTK) -t join $(outdir)/Sample/*classIII.stat.xls > $(outdir)/allsample.pathway.III.stat.tmp.xls
	$(PYTHON3) $(BIN)/script/del_repeat_col.py -i $(outdir)/allsample.pathway.II.stat.tmp.xls -o $(outdir)/allsample.pathway.II.stat.xls -r ClassI
	$(PYTHON3) $(BIN)/script/del_repeat_col.py -i $(outdir)/allsample.pathway.III.stat.tmp.xls -o $(outdir)/allsample.pathway.III.stat.tmp.tmp.xls -r ClassIII
	$(PYTHON3) $(BIN)/script/del_repeat_col.py -i $(outdir)/allsample.pathway.III.stat.tmp.tmp.xls -o $(outdir)/allsample.pathway.III.stat.tmp.tmp.tmp.xls -r ClassII
	$(PYTHON3) $(BIN)/script/del_repeat_col.py -i $(outdir)/allsample.pathway.III.stat.tmp.tmp.tmp.xls -o $(outdir)/allsample.pathway.III.stat.xls -r ClassI
	@echo "===================== Run pathway stat End at `date` ===================== "

pathway_plot:
	@echo "===================== Run pathway_plot End at `date` ===================== "
	[ -d $(outdir) ] && rm -rf $(outdir) || echo ok
	mkdir -p $(outdir)
	$(Rscript) $(BIN)/script/draw_pathway.r $(infile) $(outdir)/$(prefix).pdf
	$(CONVERT) $(outdir)/$(prefix).pdf $(outdir)/$(prefix).png
	@echo "===================== Run pathway_plot End at `date` ===================== "

BIN=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
include $(config)

user=admin
type=cloud
ip=192.168.1.3

HELP:
	@echo Description: 此脚本用于生成结题报告
	@echo Usage :
	@echo [***Get_report_conf说明]:获取report.config文件
	@echo make -f makefile config= project_conf= outfile= upload_dir= Get_report_conf
	@echo [参数说明]:
	@echo -e "config       : [必选]流程配置文件"
	@echo -e "project_conf : [必选]项目配置文件"
	@echo -e "outfile      : [必选]输出结果文件"
	@echo -e "upload_dir   : [必选]report/upload目录，主要用于生成report.config文件中的Report_dir"
	@echo [***Get_Upload说明]:整理upload目录
	@echo make -f makefile config= project_conf= template= outdir= Get_Upload
	@echo [参数说明]:
	@echo -e "config       : [必选]流程配置文件"
	@echo -e "project_conf : [必选]项目配置文件"
	@echo -e "template     : [必选]结题报告模板一般为BIN/config/template.txt"
	@echo -e "upload_config: [必选]结题报告整理目录配置文件，一般为BIN/config/upload.conf"
	@echo -e "outdir       : [必选]结题报告路径，一般为Analysis/report"
	@echo -e "\n"[***Report说明]:生成结题报告
	@echo make -f makefile config= outdir= template= report_conf= Report
	@echo [参数说明]:
	@echo -e "outdir      : [必选]输出目录（结题报告目录），一般为Analysis/report，会在该目录下生成结题报告文件以及report.sh，可以再次运行更新报告内容"
	@echo -e "template    : [必选]流程中结题报告模板，包含所有模块（为Get_upload模块调整后的模板文件）"
	@echo -e "report_conf : [必选]项目报告配置文件，一般为report/report.conf文件，由Get_upload步骤生成"
	@echo -e "user        : [可选]默认admin"
	@echo -e "type        : [可选]结题报告生成选择的类型，可选cloud和local，一般使用cloud速度比较快"
	@echo -e "ip          : [可选]结题报告生成节点，默认为192.168.1.3"

	@echo -e "\n"[***pipeline_record说明]:流程运行记录存入lims数据库
	@echo make -f makefile config= project_id= analysis_dir= pipeline_record
	@echo [参数说明]:
	@echo -e "config       : [必选]流程配置文件"
	@echo -e "project_id   : [必选]子项目编号，如果是测试项目可以使用一些特殊的子项目编号，例如test,PM-001"
	@echo -e "analysis_dir : [必选]项目分析路径"


outdir=$(dir $(abspath $(firstword $(outfile))))
Get_report_conf:
	@echo "===================== Get_report_conf  Begin at `date` ===================== "
	mkdir -p $(outdir)
	$(PYTHON3) $(BIN)/script/report_conf.py -c $(project_conf) -o $(outfile) -u $(upload_dir)
	@echo "===================== Get_report_conf  End at `date` ===================== "

.PHONY:Get_Upload
Get_Upload:
	@echo "===================== get upload  Begin at `date` ===================== "
	mkdir -p $(outdir)/upload
	$(PYTHON3) $(get_upload) -c $(upload_config) -o $(outdir) -i $(indir) -t $(template) -b $(BIN) -d public-picture -n
	@echo "===================== get upload  End at `date` ===================== "

.PHONY:Report
Report:
	@echo "===================== Report  Begin at `date` ===================== "
	echo generate report start at `date`
	echo 'ssh $(ip)  $(report_python3) $(report_py) -i $(template) -c $(report_conf) -u $(user) -t $(type)' >$(outdir)/report.sh
	cd $(outdir) && ssh $(ip) $(report_python3) $(report_py) -i $(template) -c $(report_conf) -u $(user) -t $(type)
	@echo "===================== Report  End at `date` ===================== "
	echo generate report end at `date`

pipeline_record:
	@echo "===================== pipeline_record  Begin at `date` ===================== "
	$(PYTHON3) $(BIN)/script/pipeline_stat.py -p $(project_id) -d $(analysis_dir) -c $(config)
	@echo "===================== pipeline_record  Begin at `date` ===================== "

#日志模式
logmode = "print"  # all | file | print | null
#开启parallel后才可以跑level=1的case，关闭只能跑level=0的case
parallel = True
#如果parallel开启，并且casemode是all时，先跑level=1的case，然后跑case=0的case
#casemode=parallel  只跑level=1的case，多线程跑
#casemode=serial	只跑level=0的case
casemode = "serial"  # all | parallel | serial
#调试case时打开，生产环境关闭
debug = False
#用例存放文件目录
casedir = '/data/1v1_case_serial'
#casedir = '/data/1v1_case_parallel'
#日志和报告存放文件目录
filepath = '/data/defender_Serial'
#filepath = '/data/defender_parallel'

server = "10.2.1.68"
#日志查看服务端口
serverport = 8081
#serverport = 8082
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<[gunicorn配置]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import multiprocessing

bind = "0.0.0.0:%s" %serverport 

workers = multiprocessing.cpu_count()*2 + 1

worker_class = "sync"

reload = True

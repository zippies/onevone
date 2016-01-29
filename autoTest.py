import os,sys,time
sys.path.append('main')
from multiprocessing import Manager
from datetime import datetime
from jinja2 import Template
from configs import logmode,parallel,casemode,debug,casedir,filepath,server,serverport
sys.path.append(casedir)

class Runner(object):
	def __init__(self,looptime=1,singlecase=None,buildname=''):
		self.casefiles = [file[:-3] for file in os.listdir(casedir) if file.endswith('.py')]
		self.casefiles.sort()
		self.testcases = [__import__(casefile).TestCase() for casefile in self.casefiles]
		self.caseCount = len(self.testcases) if not singlecase else 1
		self.failedCases = []
		self.singlecase = singlecase
		self.buildname = buildname
		self.logdir = os.path.join(filepath,"logs","L"+str(looptime)+"_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
		self.reportdir = os.path.join(filepath,"reports",buildname)
		self.result = {
			"casecount":0,
			"failed":[],
			"passed":[],
			"runtime":0,
			"loop":looptime
		}
		self._initLogPath()

	def getdescs(self):
		print("%3s  %8s  %s" %('id','name','desc'))
		for index,case in enumerate(self.testcases):
			name = str(case.__class__).split('.')[0].split('\'')[1]
			print('%3s  %8s  %s' %(index+1,name,case.desc))

	def collectResult(self,case):
		result = {"name":case.name,"desc":case.desc,"endtime":case.endtime,"logpath":case.logpath+'.info',"errorMsg":case.result['error']}

		if not case.result['result']:
			self.result['failed'].append(result)
		else:
			self.result['passed'].append(result)

		if not parallel:
			self.result['runtime'] += round(case.result['runtime'],2)

	def _initLogPath(self):
		if not os.path.isdir(self.logdir) and logmode not in ['print','null']:
			os.makedirs(self.logdir)
		if not os.path.isdir(self.reportdir):
			os.makedirs(self.reportdir)

	def _initCase(self,case,level=0):
		name = str(case.__class__).split('.')[0].split('\'')[1]
		logpath = os.path.join(self.logdir,name) if os.path.isdir(self.logdir) else ''
		result = Manager().dict()
		setattr(case,'result',result)
		setattr(case,'logpath',logpath)
		setattr(case,'debug',debug)
		setattr(case,'logmode',logmode)
		setattr(case,'name',name)
		setattr(case,'level',level)
		return case

	def getReportContent(self):
		try:
			with open('main/report_template.html','r') as f:
				return f.read()
		except:
			return ''

	def generateReport(self):
		content = self.getReportContent()
		template = Template(content)
		html = template.render(result=self.result,server=server,serverport=serverport)
		report = os.path.join(self.reportdir,'report.html')
		print(report)
		with open(report,'w') as f:
			f.write(html)

	def runTest(self):
		parallelcases = []
		serialcases = []
		for case in self.testcases:
			modifiedcase = None
			if not hasattr(case, 'level') or case.level == 0:
				modifiedcase = self._initCase(case)
				if self.singlecase and self.singlecase != modifiedcase.name:
					continue

				serialcases.append(modifiedcase)
			else:
				modifiedcase = self._initCase(case,1)
				if self.singlecase and self.singlecase != modifiedcase.name:
					continue

				parallelcases.append(modifiedcase)

			if self.singlecase:
				break

		if parallel:
			if casemode == 'all':
				self.runParallel(parallelcases)
				self.runSerial(serialcases)
			elif casemode == 'parallel':
				self.runParallel(parallelcases)
			elif casemode == 'serial':
				self.runSerial(serialcases)
		else:
			self.runSerial(serialcases)
		
		self.generateReport()

	def runParallel(self,parallelcases):
		starttime = time.time()

		for case in parallelcases:
			case.start()

		for case in parallelcases:
			case.join()
			setattr(case,'endtime',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			if not case.result['result']:
				print("case: %s.py failed" %case.name)
				print("    logpath:%s" %case.logpath)
				print("    errorMsg:%s" %case.result['error'])

		for case in parallelcases:
			self.collectResult(case)

		self.result['casecount'] = len(parallelcases)
		self.result['runtime'] = round(time.time() - starttime,2)

	def runSerial(self,serialcases):
		for case in serialcases:
			print("running testcase:%s,desc:%s" %(case.name,case.desc))
			case.start()
			case.join()
			print("    [finished with]: %s, logpath: %s, errorMsg: %s" %(case.result['result'],case.logpath,case.result['error']))
			setattr(case,'endtime',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			self.collectResult(case)

		self.result['casecount'] = len(serialcases)


if __name__ == '__main__':
	import sys
	from pprint import pprint
	casename = None
	loop = 1
	buildname = ''

	try:
		loop = int(sys.argv[1])
		try:
			buildname = sys.argv[2]
		except IndexError:
			pass
	except IndexError:
		pass
	except Exception as e:
		if sys.argv[1] == 'getdescs':
			runner = Runner(casename)
			runner.getdescs()
			sys.exit(0)
		casename = sys.argv[1]

	for i in range(loop):
		runner = Runner(i+1,casename,buildname)
		runner.runTest()
		assert len(runner.result['failed']) == 0,"Build Marked As Failed!"
		#pprint(runner.result)

			
			
			

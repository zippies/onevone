from onevone.basecase import BaseCase,CheckError,testcase

class TestCase(BaseCase):
	level = 1
	desc = "老师请求结束讲解还未收到成功回调时，老师杀进程，学生是否能收到老师peerdisconnect和endexplain通知"
	caseData = {
		'students' : ['11266660166'],
		'teachers' : ['11166660166'],
		'st_passwd' : '96E79218965EB72C92A549DD5A330112',
		'tc_passwd' : '96e79218965eb72c92a549dd5a330112',
		'server' : 'http://180.150.184.115:180/',
		'imgurl' : 'http://wenba-img.ufile.ucloud.com.cn/u-20150930-02b5c27e-bc9b-47ce-b8f5-52fe879eda89.png'
	}

	def __init__(self):
		BaseCase.__init__(self)

	@testcase(caseData)
	def run(self):
		self.login(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],['st_onlogin']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onlogin'])
		assert self.checkCallbacks(self.teachers[0],['tc_onlogin']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onlogin'])
		self.clearCallbacks()
		
		self.setfree(self.teachers)

		self.submitquestion(self.students)
		
		assert self.checkCallbacks(self.teachers[0],['tc_onsetteacherstat','tc_onnotifyneworder']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onsetteacherstat','tc_onnotifyneworder'])
		assert self.checkCallbacks(self.students[0],['st_onsubmitquestion']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onsubmitquestion'])
		self.clearCallbacks()
		
		storderNo = self.getStOrderNo(self.students[0])
		self.graborder(self.teachers,storderNo,setbusy=True)
		
		self.sleep(3)

		assert self.checkCallbacks(self.students[0],['st_onnotifygraborder', 'st_onnotifyorderresult']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotifygraborder', 'st_onnotifyorderresult'])
		self.clearCallbacks()

		tcorderNo = self.getTcOrderNo(self.teachers[0])
		
		assert tcorderNo == storderNo,"student orderNo:%s not equals teacher grabbed orderNo:%s" %(storderNo,tcorderNo)
		
		self.createvoicechannel(self.teachers+self.students)
		
		assert self.checkCallbacks(self.students[0],['st_oncreatevoicechannel']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_oncreatevoicechannel'])
		assert self.checkCallbacks(self.teachers[0],['tc_oncreatevoicechannel']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_oncreatevoicechannel'])
		self.clearCallbacks()
		
		self.newmedia(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],[])
		assert self.checkCallbacks(self.teachers[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],[])
		self.clearCallbacks()
		
		self.connectmedia(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],[])
		assert self.checkCallbacks(self.teachers[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],[])
		self.clearCallbacks()
		
		self.enterroom(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],[])
		assert self.checkCallbacks(self.teachers[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],[])
		self.clearCallbacks()
		
		self.enterroomresult(self.teachers+self.students)

		self.waitCallback(self.students[0],'st_onnotifystartanalyzequestion')
		self.waitCallback(self.teachers[0],'tc_onnotifystartanalyzequestion')
		assert self.checkCallbacks(self.students[0],['st_onnotifystartanalyzequestion','st_onenterroomresult']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotifystartanalyzequestion','st_onenterroomresult'])
		assert self.checkCallbacks(self.teachers[0],['tc_onnotifystartanalyzequestion','tc_onenterroomresult']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onnotifystartanalyzequestion','tc_onenterroomresult'])
		self.clearCallbacks()
		
		self.startaction(self.teachers+self.students)

		self.beginexplain(self.teachers)
		assert self.checkCallbacks(self.students[0],['st_onnotifytcbeginexplain', 'st_onnotify_openstream']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotifytcbeginexplain','st_onnotify_openstream'])
		assert self.checkCallbacks(self.teachers[0],['tc_onbeginexplain', 'tc_onnotify_openstream']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onbeginexplain', 'tc_onnotify_openstream'])
		self.clearCallbacks()
		
		self.suspendexplain(self.students)
		assert self.checkCallbacks(self.students[0],['st_onsuspendexplain']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onsuspendexplain'])
		assert self.checkCallbacks(self.teachers[0],['tc_onnotifystsuspendexplain']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onnotifystsuspendexplain'])
		self.clearCallbacks()
		self.sleep(2)
		self.endexplain(self.teachers,nowait=True)
		self.sleep(0.2)
		self.kill(self.teachers)
		self.waitCallbacks(self.students,'st_onnotifytcendexplain')

		self.stopaction(self.students,nowait=True)

		self.sleep(2)

		self.leaveroom(self.students,nowait=True)

		self.sleep(2)
		
		self.closemedia(self.students,nowait=True)
		
		self.sleep(60)

		self.logout(self.students)
		if 'st_onnotifypeerdisconnect' in self.callbacks['student'][self.students[0]]:
			assert self.checkCallbacks(self.students[0],['st_onnotifypeerdisconnect','st_onnotifytcendexplain','st_onlogout']) is True,"receive unexpect callbacks\
			:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotifypeerdisconnect','st_onnotifytcendexplain','st_onlogout'])
		else:
			assert self.checkCallbacks(self.students[0],['st_onnotifytcendexplain','st_onlogout']) is True,"receive unexpect callbacks\
			:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotifytcendexplain','st_onlogout'])

		self.clearCallbacks()

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

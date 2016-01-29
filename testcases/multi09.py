from onevone.basecase import BaseCase,CheckError,testcase

class TestCase(BaseCase):
	level = 1
	desc = "老师开始讲解后学生暂停讲解15秒后恢复讲解，老师结束讲解"
	caseData = {
		'students' : ['11266660109'],
		'teachers' : ['11166660109'],
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

		self.waitCallback(self.students[0],'st_onnotifystartanalyzequestion',30)
		self.waitCallback(self.teachers[0],'tc_onnotifystartanalyzequestion',30)
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
		
		self.sleep(15)
		self.recoverexplain(self.students)
		assert self.checkCallbacks(self.students[0],['st_onrecoverexplain']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onrecoverexplain'])
		assert self.checkCallbacks(self.teachers[0],['tc_onnotifystrecoverexplain']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onnotifystrecoverexplain'])
		self.clearCallbacks()

		self.endexplain(self.teachers)
		assert self.checkCallbacks(self.students[0],['st_onnotifytcendexplain']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotifytcendexplain'])
		assert self.checkCallbacks(self.teachers[0],['tc_onendexplain']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onendexplain'])
		self.clearCallbacks()
		
		self.stopaction(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],['st_onnotify_closestream']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onnotify_closestream'])
		assert self.checkCallbacks(self.teachers[0],['tc_onnotify_closestream']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onnotify_closestream'])
		self.clearCallbacks()
		
		self.leaveroom(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],[])
		assert self.checkCallbacks(self.teachers[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],[])
		self.clearCallbacks()
		
		self.closemedia(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],[])
		assert self.checkCallbacks(self.teachers[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],[])
		self.clearCallbacks()
		
		self.logout(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],['st_onlogout']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onlogout'])
		assert self.checkCallbacks(self.teachers[0],['tc_onlogout']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onlogout'])
		self.clearCallbacks()

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

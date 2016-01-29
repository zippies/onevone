from onevone.basecase import BaseCase,CheckError,testcase

class TestCase(BaseCase):
	level = 1
	desc = "抢单过程中学生杀进程，老师是否能收到学生peerdisconnect通知"
	caseData = {
		'students' : ['11266660156'],
		'teachers' : ['11166660156'],
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

		self.graborder(self.teachers,storderNo,setbusy=True,nowait=True)
		self.kill(self.students)

		tcorderNo = self.getTcOrderNo(self.teachers[0],timeout=30)
		
		assert tcorderNo == storderNo,"student orderNo:%s not equals teacher grabbed orderNo:%s" %(storderNo,tcorderNo)

		self.waitCallbacks(self.teachers,'tc_onnotifypeerdisconnect',60)

		self.logout(self.teachers)
		if 'tc_onsetteacherstat' in self.callbacks['teacher'][self.teachers[0]]:
			assert self.checkCallbacks(self.teachers[0],['tc_onsetteacherstat','tc_ongraborder','tc_onnotifypeerdisconnect','tc_onlogout']) is True,"receive unexpect callbacks\
			:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onsetteacherstat','tc_ongraborder','tc_onnotifypeerdisconnect','tc_onlogout'])
		else:
			assert self.checkCallbacks(self.teachers[0],['tc_ongraborder','tc_onnotifypeerdisconnect','tc_onlogout']) is True,"receive unexpect callbacks\
			:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_ongraborder','tc_onnotifypeerdisconnect','tc_onlogout'])
			self.clearCallbacks()


		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

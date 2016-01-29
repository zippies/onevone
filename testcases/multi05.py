from onevone.basecase import BaseCase,CheckError,testcase

class TestCase(BaseCase):
	level = 1
	desc = "老师抢单后学生未进入房间"
	caseData = {
		'students' : ['11266660105'],
		'teachers' : ['11166660105'],
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
		
		self.enterroom(self.teachers)
		assert self.checkCallbacks(self.students[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],[])
		assert self.checkCallbacks(self.teachers[0],[]) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],[])
		self.clearCallbacks()
		
		self.enterroomresult(self.teachers)

		r = self.waitCallbacks(self.teachers,'tc_onnotifystartanalyzequestion',50)[0][0]
		assert r.res.code != 0,"学生未进入房间，审题通知不应为0,return code:%s,errorMsg:%s" %(r.res.code,r.res.errorMsg.decode())
		
		self.waitCallbacks(self.students,'st_onnotifytccancelorder')
		self.clearCallbacks()
		
		self.logout(self.teachers+self.students)
		assert self.checkCallbacks(self.students[0],['st_onlogout']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['student'][self.students[0]],['st_onlogout'])
		assert self.checkCallbacks(self.teachers[0],['tc_onlogout']) is True,"receive unexpect callbacks\
		:received callbacks:%s,expected callbacks:%s" %(self.callbacks['teacher'][self.teachers[0]],['tc_onlogout'])
		self.clearCallbacks()

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

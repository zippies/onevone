#学生拥有的方法锁
st_codeActions = ['starts','login','relogin','disconnect','submitquestion','createvoicechannel','cancelorder','newmedia','connectmedia','enterroom','enterroomresult','startaction','uploaddata','stopaction','leaveroom','suspendexplain','closemedia','recoverexplain','endexplain','logout','stops','clear']
#老师拥有的方法锁
tc_codeActions = ['starts','login','disconnect','setfree','setbusy','graborder','regretorder','createvoicechannel','beginexplain','startaction','newmedia','connectmedia','enterroom','enterroomresult','uploaddata','stopaction','leaveroom','closemedia','endexplain','logout','stops','clear']

#codeAction对应的检查点
tc_checklist_mapper = {
        'starts':[('isstart',None)],
        'login':[('isstart',None),('islogin',None)],
	'setfree':[('islogin',None),('isfree',None)],
	'setbusy':[('islogin',None),('isbusy',None)],
        'graborder':[('isonline',None),('isgraborder',None),('isnotifygraborder','expected'),('isnforderresult','expected')],
        'regretorder':[('isonline',None),('isregretorder',None),('isnotifytccancelorder','expected')],
        'createvoicechannel':[('isonline',None),('iscreatevoicechannel',None)],
        'beginexplain':[('isonline',None),('istcbeginexplain',None),('isnotifytcbgexplain','expected')],
        'newmedia':[('isonline',None),('isnewmedia',None)],
        'connectmedia':[('isonline',None),('isconnectmedia',None)],
        'enterroom':[('isonline',None),('isenterroom',None)],
	'enterroomresult':[('isenterroomsuccess',None)],
        'startaction':[('isonline',None),('isstartaction',None)],
        'uploaddata':[('isonline',None),('isuploaddata',None)],
        'stopaction':[('isonline',None),('isstopaction',None),('isnotifyclosestream','expected')],
        'leaveroom':[('isonline',None),('isleaveroom',None)],
        'closemedia':[('isonline',None),('isclosemedia',None)],
        'endexplain':[('isonline',None),('istcendexplain',None),('isnotifytcendexplain','expected')],
        'logout':[('isonline',None),('islogout',None)],
	'disconnect':[('isonline',None),('isdisconnect',None)],
        'stops':[('isstop',None)]
}

#执行学生动作后需要检查的学生状态
st_checklist_mapper = {
        'starts':[('isstart',None)],
        'login':[('isstart',None),('islogin',None)],
	'relogin':[('isrelogin',None)],
        'submitquestion':[('isonline',None),('issubmitquestion',None),('isnotifyneworder','any')],
        'cancelorder':[('isonline',None),('iscancelorder',None),('isnotifystcancelorder','expected')],
        'createvoicechannel':[('isonline',None),('iscreatevoicechannel',None)],
        'newmedia':[('isonline',None),('isnewmedia',None)],
        'connectmedia':[('isonline',None),('isconnectmedia',None)],
        'enterroom':[('isonline',None),('isenterroom',None)],
	'enterroomresult':[('isenterroomsuccess',None)],
        'startaction':[('isonline',None),('isstartaction',None)],
        'uploaddata':[('isonline',None),('isuploaddata',None)],
        'stopaction':[('isonline',None),('isstopaction',None),('isnotifyclosestream','expected')],
        'leaveroom':[('isonline',None),('isleaveroom',None)],
        'closemedia':[('isonline',None),('isclosemedia',None)],
        'suspendexplain':[('isonline',None),('isstsuspendedexplain',None),('isnotifystsuspendexplain','expected')],
        'recoverexplain':[('isonline',None),('isstrecoverexplain',None),('isnotifystrecoverexplain','expected')],
        'endexplain':[('isonline',None),('isstendexplain',None),('isnotifystendexplain','expected')],
        'logout':[('isonline',None),('islogout',None)],
	'disconnect':[('isonline',None),('isdisconnect',None)],
        'stops':[('isstop',None)]
}

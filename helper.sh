if [[ $1 = 'p1' ]]; then
	for i in `seq $2 $3`
	do
		curl -X POST http://10.2.1.68:8080/job/1v1_automation_p1/$i/doDelete
		echo "Deleted build:$i"
	done
	echo 1 > /root/.jenkins/jobs/1v1_automation_p1/nextBuildNumber
	curl -X POST http://10.2.1.68:8080/job/1v1_automation_p1/reload
	echo "Build Reload Success!"
elif [[ $1 = 'p2' ]]; then
	for i in `seq $2 $3`
	do
		curl -X POST http://10.2.1.68:8080/job/1v1_automation_p2/$i/doDelete
		echo "Deleted build:$i"
	done
	echo 1 > /root/.jenkins/jobs/1v1_automation_p2/nextBuildNumber
	curl -X POST http://10.2.1.68:8080/job/1v1_automation_p2/reload
	echo "Build Reload Success!"
elif [[ $1 = 's1' ]]; then
	for i in `seq $2 $3`
	do
		curl -X POST http://10.2.1.68:8080/job/1v1_automation_s1/$i/doDelete
		echo "Deleted build:$i"
	done
	echo 1 > /root/.jenkins/jobs/1v1_automation_s1/nextBuildNumber
	curl -X POST http://10.2.1.68:8080/job/1v1_automation_s1/reload
	echo "Build Reload Success!"
elif [[ $1 = 's2' ]]; then
	for i in `seq $2 $3`
	do
		curl -X POST http://10.2.1.68:8080/job/1v1_automation_s2/$i/doDelete
		echo "Deleted build:$i"
	done
	echo 1 > /root/.jenkins/jobs/1v1_automation_s2/nextBuildNumber
	curl -X POST http://10.2.1.68:8080/job/1v1_automation_s2/reload
	echo "Build Reload Success!"
elif [[ $1 = 'run' ]]; then
	gunicorn -c configs.py collector:app
elif [[ $1 = 'runnohup' ]]; then
	nohup gunicorn -c configs.py collector:app >/dev/null &
else
	rm -rf main/history/2015*.png __pycache__ main/__pycache__ main/onevone/cstructs/__pycache__ nohup.out main/onevone/__pycache__
fi

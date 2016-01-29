from flask import Flask,render_template,request,jsonify
from configs import filepath,serverport,casedir
import os

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/view/<path>/<file>')
def viewlog(path,file):
	errorinfo = ""
	logname = os.path.join(path,file)
	error = os.path.join(filepath,'logs',path,file[:-4]+'error')
	with open(error,'r') as f:
		errorinfo = f.read()

	return render_template('viewlog.html',casename=file,logname=logname,errorinfo=errorinfo)

@app.route('/getcase/<file>')
def getcase(file):
	casefile = os.path.join(casedir,file[:-4] + 'py')
	with open(casefile,'r') as f:
		return f.read()

@app.route('/getlog/<path>/<file>')
def getlog(path,file):
	logfile = os.path.join(filepath,'logs',path,file)
	with open(logfile,'r') as f:
		return f.read().strip()

@app.route("/savecase",methods=['POST'])
def savecase():
	content = request.form.get("content")
	case = request.form.get("case")
	if content:
		casefile = os.path.join(casedir,case[:-4] + 'py')
		try:
			with open(casefile,'w') as f:
				f.write(content)
		except Exception as e:
			return jsonify({"result":False,"msg":str(e)})

	return jsonify({"result":True,"msg":"ok!"})

if __name__ == '__main__':
	app.run('0.0.0.0',port=serverport)

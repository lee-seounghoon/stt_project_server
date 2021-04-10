#작성자 : 이승훈
#졸업프로젝트에서 사용하였던 서버프로그램의 코드입니다. 사용한 프레임워크는 플라스크입니다.

#-*- coding: utf-8 -*-

import os
import subprocess
import sys
from flask import Flask, render_template, request
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
professor = {\
"교수님 성함":["교수님연구실", "교수님이메일","연구실전화번호","관심과목","출신학교"] \
}


@app.route("/")
def index():
	return render_template("upload.html")

#사람의 음성파일을 받는 방식이 2가지였는데 1. 웹페이지상의 녹음기로 녹음된 음성파일을 보내는 경우 2. 처음부터 녹음된 음성파일을 업로드하는 경우였고 recload의 경우는 1의 경우에 해당합니다. 파이어폭스와 크롬에 대해서 대처할 수 있도록 try와 exception을 이용했습니다. 웹페이지상에서 녹음이 진행될 경우 브라우저의 종류에 따라 다른 형식으로 음성파일이 전송되어 오는데 이 파일을 구별하기가 쉽지 않아서 오류가 나면 다른 브라우저형식인것을 전제로 코드를 짰습니다.pydub을 이용해서 업로드된 파일을 인코딩도 해주었습니다.
@app.route("/recload", methods=['POST'])
def recload():
	try:
		f = request.files['audio']
		with open('images/audio.ogg', 'wb') as audio:
			f.save(audio)
		filename = "audio.ogg"
		print(filename)
		target = os.path.join(APP_ROOT, 'images')
		print(target)
		destination = "/".join([target, filename])
		print(destination)

		#remove existing file
		subprocess.call('rm ~/LEESH/testdata/test.wav', shell=True)

		#convert uploadfile to wav
		file_extension = filename.split('.')
		m4a_file = AudioSegment.from_file(file = destination, format = file_extension[1])
		#m4a_file = AudioSegment.from_wav(file = destination)
		print(m4a_file.sample_width)
		m4a_file = m4a_file.set_sample_width(2)
		m4a_file = m4a_file.set_channels(1)
		m4a_file = m4a_file.set_frame_rate(16000)
		m4a_file.export("images/test007.wav",format = "wav", bitrate = '16k')
		filename = "test007.wav"
		mvcmd = 'mv images/' + filename + ' images/test.wav'
		subprocess.call(mvcmd, shell=True)
		subprocess.call('mv images/test.wav ~/LEESH/testdata/', shell=True)
		subprocess.call('./decode_record.sh tri5 test_1 > a.txt', shell=True)
		test = subprocess.check_output(['tail', '-1', 'a.txt'])
		print(test)
		result_wlist = test.split()
		for prof_name in professor.keys():
			if prof_name in result_wlist:
				
				prof_rlist = professor[prof_name]
		

				return render_template("complete.html",testData=str(unicode(test)),RoomNumber=str(unicode(prof_rlist[0])),Email=str(unicode(prof_rlist[1])),RoomDial=str(unicode(prof_rlist[2])),Major=str(unicode(prof_rlist[3])),Univ=str(unicode(prof_rlist[4])))

		return render_template("fail.html",testData=str(unicode(test)))
	except CouldntDecodeError:
		nfilename = "audio.webm"
		print(nfilename)
		ntarget = os.path.join(APP_ROOT, 'images')
		print(ntarget)
		ndestination = "/".join([ntarget, nfilename])
		print(ndestination)
		newcmd = 'mv ' + destination + ' ' + ndestination
		subprocess.call(newcmd, shell=True)

		#remove existing file
		subprocess.call('rm ~/LEESH/testdata/test.wav', shell=True)

		#convert uploadfile to wav
		nfile_extension = nfilename.split('.')
		m4a_file = AudioSegment.from_file(file = ndestination, format = nfile_extension[1])
		#m4a_file = AudioSegment.from_wav(file = destination)
		print(m4a_file.sample_width)
		m4a_file = m4a_file.set_sample_width(2)
		m4a_file = m4a_file.set_channels(1)
		m4a_file = m4a_file.set_frame_rate(16000)
		m4a_file.export("images/test007.wav",format = "wav", bitrate = '16k')
		filename = "test007.wav"
		mvcmd = 'mv images/' + filename + ' images/test.wav'
		subprocess.call(mvcmd, shell=True)
		subprocess.call('mv images/test.wav ~/LEESH/testdata/', shell=True)
		subprocess.call('./decode_record.sh tri5 test_1 > a.txt', shell=True)
		test = subprocess.check_output(['tail', '-1', 'a.txt'])
		print(test)
		result_wlist = test.split()
		for prof_name in professor.keys():
			if prof_name in result_wlist:
				
				prof_rlist = professor[prof_name]
		

				return render_template("complete.html",testData=str(unicode(test)),RoomNumber=str(unicode(prof_rlist[0])),Email=str(unicode(prof_rlist[1])),RoomDial=str(unicode(prof_rlist[2])),Major=str(unicode(prof_rlist[3])),Univ=str(unicode(prof_rlist[4])))

		return render_template("fail.html",testData=str(unicode(test)))

#이 경우는 2의 경우로 이미 녹음된 음성데이터를 업로드시켜 인식시킬 때 사용한 경우입니다.
@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images')
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)

	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		print(filename)
		destination = "/".join([target, filename])
		print(destination)
		file.save(destination)
	
	#remove existing file
	subprocess.call('rm ~/LEESH/testdata/test.wav', shell=True)

	#convert uploadfile to wav
	file_extension = filename.split('.')
	m4a_file = AudioSegment.from_file(file = destination, format = file_extension[1])
	print(m4a_file.sample_width)
	m4a_file = m4a_file.set_sample_width(2)
	m4a_file = m4a_file.set_channels(1)
	m4a_file = m4a_file.set_frame_rate(16000)
	m4a_file.export("images/test007.wav",format = "wav", bitrate = '16k')
	filename = "test007.wav"
	mvcmd = 'mv images/' + filename + ' images/test.wav'
	subprocess.call(mvcmd, shell=True)
	subprocess.call('mv images/test.wav ~/LEESH/testdata/', shell=True)
	subprocess.call('./decode_record.sh tri5 test_1 > a.txt', shell=True)
	test = subprocess.check_output(['tail', '-1', 'a.txt'])
	print(test)
	result_wlist = test.split()
	for prof_name in professor.keys():
		if prof_name in result_wlist:
			
			prof_rlist = professor[prof_name]
	

			return render_template("complete.html",testData=str(unicode(test)),RoomNumber=str(unicode(prof_rlist[0])),Email=str(unicode(prof_rlist[1])),RoomDial=str(unicode(prof_rlist[2])),Major=str(unicode(prof_rlist[3])),Univ=str(unicode(prof_rlist[4])))

	return render_template("fail.html",testData=str(unicode(test)))
if __name__=='__main__':
	app.run(port=4555, debug=True)

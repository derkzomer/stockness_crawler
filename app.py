from flask import Flask,render_template,request,redirect
import csv,time

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

def read():
	keywords = open('keywords.txt', 'r') .read()
	return keywords

@app.route('/',methods=["GET", "POST"])
def index():
	if request.method == 'GET':
		keywords = read()
		return render_template('index.html', success=False, keywords=keywords)
	else:
		data = request.form['keywords']
		with open('keywords.txt',"wb") as fo:
			fo.write(data)
			success = True
		keywords = read()
		return render_template('index.html', success=True, keywords=keywords)
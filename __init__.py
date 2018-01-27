from flask import Flask,render_template,request,redirect
import csv,time

app = Flask(__name__)
#app.run(host='0.0.0.0')
#app.config['DEBUG'] = True

FLASK_DEBUG=1

def read():
	keywords = open('/var/www/stocknesscrawler/keywords.txt', 'r') .read()
	return keywords

@app.route('/',methods=["GET", "POST"])
def index():
	if request.method == 'GET':
		keywords = read()
		return render_template('index.html', success=False, keywords=keywords)
	else:
		data = request.form['keywords']
		with open('/var/www/stocknesscrawler/keywords.txt',"wb") as fo:
			fo.write(data)
			success = True
		keywords = read()
		return render_template('index.html', success=True, keywords=keywords)

if __name__ == "__main__":
	app.run()

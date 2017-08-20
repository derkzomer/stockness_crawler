from bs4 import BeautifulSoup
import requests,csv,smtplib,datetime
from email.mime.text import MIMEText
from os.path import basename
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def send_mail():

	msg = MIMEMultipart()
	msg['Subject'] = 'Stocknessmonster scrape of %s' % today 
	msg['From'] = 'derk@uber.com'
	msg['To'] = 'derkzomer@gmail.com'

	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(file, "rb").read())
	Encoders.encode_base64(part)

	part.add_header('Content-Disposition', 'attachment; filename="'+file+'"')

	text = 'Thanks for the wine.'

	msg.attach(MIMEText(text))
	msg.attach(part)

	smtp = smtplib.SMTP('smtp.gmail.com',587)
	smtp.starttls()
	smtp.login('derkzomer@gmail.com','0vtr1EaujWN1')
	smtp.sendmail(msg['From'], msg['To'], msg.as_string())
	smtp.close()

url = "http://stocknessmonster.com/news-today?E=ASX"
request_object = requests.get(url)

soup = BeautifulSoup(request_object.content,"html.parser")

today = datetime.date.today()

file = 'scrape-' + str(today) + '.csv'

keywords_file = open('keywords.txt', 'r') .read()
keywords = keywords_file.split(",")

rows = []

for tr in soup.find_all('tr'):
	data = []
	for time in tr.find_all('td')[0]:
		data.append(time)
	for a in tr.find_all('a',href=True):
		data.append('http://stocknessmonster.com' + a['href'])
		data.append(a.text)

	rows.append(data)

del rows[:6]
results = []

try:
	for row in rows:
		# print row[4]
		for keyword in keywords:
				if keyword in row[4].lower():
					results.append(row)
except IndexError:
	pass

with open(file, "wb") as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	for line in results:
		writer.writerow(line)

send_mail()
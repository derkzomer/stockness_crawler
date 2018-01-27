from bs4 import BeautifulSoup,SoupStrainer
import requests,csv,smtplib,datetime
from email.mime.text import MIMEText
from os.path import basename
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def send_mail():

	msg = MIMEMultipart()
	msg['Subject'] = 'Stocknessmonster scrape of %s' % today 
	msg['From'] = 'derkzomer@gmail.com'
	msg['To'] = 'njwhite@deloitte.com.au'
	#msg['To'] = 'derkzomer@gmail.com'

	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(file, "rb").read())
	Encoders.encode_base64(part)

	part.add_header('Content-Disposition', 'attachment; filename="'+file+'"')

	text = 'Thanks for the wine. You can change keywords at http://stocknesscrawler.derkzomer.com.au/. You get emailed the results every morning at 9:30am. CYC'

	msg.attach(MIMEText(text))
	msg.attach(part)

	smtp = smtplib.SMTP('smtp.gmail.com',587)
	smtp.starttls()
	smtp.login('derkzomer@gmail.com','qm6WOyj4i*53l0')
	smtp.sendmail(msg['From'], msg['To'], msg.as_string())
	smtp.close()

url = "http://stocknessmonster.com/news-today?E=ASX"
request_object = requests.get(url)

soup = BeautifulSoup(request_object.content,"html.parser")

today = datetime.date.today()

file = '/var/www/stocknesscrawler/scrape-' + str(today) + '.csv'

keywords_file = open('/var/www/stocknesscrawler/keywords.txt', 'r') .read()
keywords = keywords_file.split(",")

rows = []

data_table = soup.find_all('table')


for tr in data_table[4].find_all('tr'):
	data = []
	data.append(tr.find_all('td')[0].text)
	data.append(tr.find_all('td')[1].text)
	data.append(tr.find_all('td')[2].text)
	try:
		data.append('http://stocknessmonster.com' + tr.find_all('td')[2].find('a')['href'])
	except:
		pass
	rows.append(data)

results = []

for row in rows:
	for keyword in keywords:
		if keyword.lower() in row[2].lower():
			results.append(row)

with open(file, "wb") as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	for line in results:
		writer.writerow(line)

send_mail()

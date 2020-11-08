from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import smtplib, ssl
from email.mime.text import MIMEText

#python -m smtpd -c DebuggingServer -n localhost:1025

#variables and URL setup
max_price = 850
min_price = 500
graphicsCard = "RTX 3080"
url = 'https://www.amazon.com/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82'
#url = 'https://www.amazon.com/stores/page/26BBE2FD-3BC3-4057-9F6A-E7DCF1EB3838?ingress=0&visitId=96849d5c-3b40-49f5-a0b6-790f42c684ac'

print(url)

# email setup 64.233.184.108
port = 587
smtp_server = 'smtp.gmail.com'
email = 'nica.dev2020@gmail.com'
password = "Carp_1017"
context = ssl.create_default_context()
sender = 'email@gmail.com'
reciever = 'email@gmail.com'


#gets page and parses html
page = uReq(url)
page_html = page.read()
page.close()
page_soup = soup(page_html, "html.parser")

#grab all product containers
containers = page_soup.findAll("li", {"class":"style__fixed__k9Vjk"})
print(containers)

#loop through each container
for i in range(0, len(containers)):
	container = containers[i]

	#grab item title and url
	# titleContainer = container.findAll("a", {"class":"item-title"})
	# productName = titleContainer[0].text.strip()
	# itemURL = container.findAll('a', {'class':'item-img'})[0]['href']

	#grab item price
	priceContainer = container.findAll("li", {"class":"price-current"})
	try:
		productPrice = priceContainer[0].text.strip().split()[0][1:].replace(',','')
		productPrice = float(productPrice)
	except IndexError:
		productPrice = 10000

	# print("-----------------------------------------------------------------\n%s" % productName)
	# print(productPrice)

    # Get status of item
	buttonContainer = container.findAll("button", {"class":"btn"}) # resultSet
	try:
		buttonStatus = buttonContainer[0]['title']
		if buttonStatus[:4] + buttonStatus[-7:] == "Add to cart":
			buttonStatus = "Add to cart"
	except IndexError:
		buttonStatus = "Not Available"

	#print("\'%s\'" % buttonStatus)

	# Create Email message
	message = "Click this link to buy: %s" % (itemURL)
	SUBJECT = graphicsCard + " IN STOCK!"
	message = MIMEText(message)
	message['Subject'] = SUBJECT
	message['To'] = email
	message['From'] = 'Newegg Bot'

	# check if item is available
	if (buttonStatus == 'View Details ' or buttonStatus == "Add to cart") and (productPrice < max_price and productPrice > min_price):
		print("<><><><> BUY <><><><>")

		# login and send email message
		# try:
		# 	server = smtplib.SMTP(smtp_server, port)
		# 	server.ehlo() # Can be omitted
		# 	server.starttls(context=context)
		# 	server.ehlo() # Can be omitted
		# 	server.login(email, password)
		# 	server.sendmail(sender, reciever, message.as_string())
		# except Exception as e:
		# 	print(e)
		# finally:
		# 	server.quit()

	else:
		print("Out of stock :(")
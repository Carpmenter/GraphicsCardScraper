from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib, ssl
from email.mime.text import MIMEText

#python -m smtpd -c DebuggingServer -n localhost:1025

#variables and URL setup
max_price = 2600
min_price = 500
graphicsCard = "RTX 3080"
frontURL = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description='
backURL = '&N=-1&isNodeId=1'
url = frontURL + graphicsCard.replace(' ', '+') + backURL

print(url)

# email setup 64.233.184.108
port = 587
smtp_server = 'smtp.gmail.com'
email = 'nica.dev2020@gmail.com'
password = "Carp_1017"
context = ssl.create_default_context()


#gets page and parses html
page = uReq(url)
page_html = page.read()
page.close()
page_soup = soup(page_html, "html.parser")

#grab all product containers
containers = page_soup.findAll("div", {"class":"item-container"})
#print(containers)

#loop through each container
for i in range(0, len(containers)):
	container = containers[i]

	#grab item title and url
	titleContainer = container.findAll("a", {"class":"item-title"})
	productName = titleContainer[0].text.strip()
	itemURL = container.findAll('a', {'class':'item-img'})[0]['href']

	#grab item price
	priceContainer = container.findAll("li", {"class":"price-current"})
	try:
		productPrice = priceContainer[0].text.strip().split()[0][1:].replace(',','')
		productPrice = float(productPrice)
	except IndexError:
		productPrice = 10000

	print("-----------------------------------------------------------------\n%s" % productName)
	print(productPrice)

    # Get status of item
	buttonContainer = container.findAll("button", {"class":"btn"}) # resultSet
	try:
		buttonStatus = buttonContainer[0]['title']
		if buttonStatus[:4] + buttonStatus[-7:] == "Add to cart":
			buttonStatus = "Add to cart"
	except IndexError:
		buttonStatus = "Not Available"

	print("\'%s\'" % buttonStatus)

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
		try:
			server = smtplib.SMTP(smtp_server, port)
			server.ehlo() # Can be omitted
			server.starttls(context=context)
			server.ehlo() # Can be omitted
			server.login(email, password)
			server.sendmail(email, email, message.as_string())
		except Exception as e:
			print(e)
		finally:
			server.quit()

	else:
		print("Out of stock :(")

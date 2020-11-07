from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#driver = webdriver.Firefox()

#URL Setup
graphicsCard = "rtx+2060"
frontURL = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description='
backURL = '&N=-1&isNodeId=1'
url = frontURL + graphicsCard + backURL

#gets page and parses html
page = uReq(url)
page_html = page.read()
page.close()
page_soup = soup(page_html, "html.parser")

#grab all product containers
containers = page_soup.findAll("div", {"class":"item-container"})

#search starts at index 4, 0-3 are ads
for i in range(4, len(containers)):
	container = containers[i]

	#grabs item title
	titleContainer = container.findAll("a", {"class":"item-title"})
	productName = titleContainer[0].text.strip()

	#grab item price
	priceContainer = container.findAll("li", {"class":"price-current"})
	try:
		productPrice = priceContainer[0].text.strip().split()[0][1:].replace(',','')
		productPrice = float(productPrice)
	except IndexError:
		productPrice = "N/A"

	print(productPrice)

    # Get status of item
	buttonContainer = container.findAll("button", {"class":"btn"}) # resultSet
	try:
		buttonStatus = buttonContainer[0]['title']
	except IndexError:
		buttonStatus = "Not Available"

	#print("\'%s\'" % buttonStatus)

	#grabs shipping price
	shippingContainer = container.findAll("li", {"class":"price-ship"})
	shippingCost = shippingContainer[0].text.strip()

	#print(productName)
	#print(productPrice)
	#print(shippingCost)

	# check for in stock and add to cart
	# if buttonStatus == 'View Details ' and productPrice < 600:
	# 	print("buy")
	# else:
	# 	print("Out of stock :( cant buy")

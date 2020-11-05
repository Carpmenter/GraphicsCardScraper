from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#driver = webdriver.Firefox()

#builds the URL
graphicsCard = "rtx+3080"
frontURL = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description='
backURL = '&N=-1&isNodeId=1'
url = frontURL + graphicsCard + backURL

#grabs the page
page = uReq(url)
page_html = page.read()
page.close()

#html parsing
page_soup = soup(page_html, "html.parser")



#grabs all product containers
containers = page_soup.findAll("div", {"class":"item-container"})

#makes a csv file
filename = "products.csv"
f = open(filename, "w")
headers = "Product_Name, Price, Shipping_Cost\n"
f.write(headers)

#search starts at index 4, 0-3 are ads
for i in range(4, len(containers)):
	container = containers[i]

	#grabs item title
	titleContainer = container.findAll("a", {"class":"item-title"})
	productName = titleContainer[0].text.strip()

	#grabs item price, might need try except
	priceContainer = container.findAll("li", {"class":"price-current"})
	productPrice = priceContainer[0].text.strip()

    #<button class="btn btn-primary btn-mini" title="Add ZOTAC GAMING GeForce RTX 2060 6GB GDDR6 192-bit Gaming Graphics Card, Super Compact, ZT-T20600K-10M to cart"></button>
	buttonContainer = container.findAll("button", {"class":"btn"})
	print(buttonContainer)

    #grabs only the item price from productPrice, discards the useless text
	productPriceList = productPrice.split()
	for x in range(len(productPriceList)):
		if "$" in productPriceList[x]:
			productPrice = productPriceList[x]
			break

	#grabs shipping price
	shippingContainer = container.findAll("li", {"class":"price-ship"})
	shippingCost = shippingContainer[0].text.strip()

	#print(productName)
	#print(productPrice)
	#print(shippingCost)

	#writes in the csv file, calls replace to get rid of commas
	f.write(productName.replace(",", "|") + "," + productPrice.replace(",", "") + "," + shippingCost.replace(",", "") + "\n")

f.close()
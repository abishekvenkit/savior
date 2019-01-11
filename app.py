from flask import Flask, render_template
import json
import math
import numpy as np
import requests
import firebase_admin
from firebase_admin import credentials, auth
from flask import abort
from flask import request

import geohash2 


#create app (uses bootstrap template)
app = Flask(__name__)

#customerId refers to a specific account
customerId = '5c33c2c3322fa06b677941ff'
apiKey = 'fa0bca11d2dce6398f771fd7ed49ba42'

cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred)


#create routes with respective template files

def getAccountId(accountType, customerId):
	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
	# sending get request and saving the response as response object
	r = requests.get(url = url)
	# extracting data in json format
	data = r.json()

	for account in data:
		if account["type"] == accountType:
			return account["_id"]
	return ""

@app.route("/purchases", methods=['GET'])
def purchases():
	idToken = request.args['idToken']
	accountType = request.args['accountType']

	#check if  token in valid
	try:
		decodedToken = auth.verify_id_token(idToken)
	except:
		return "INVALID USER TOKEN"
	uid = decodedToken['uid']

	#determine accountId of the correct account
	accountId = getAccountId(accountType, customerId)
	if accountId == "":
		return "ACCOUNT TYPE DOES NOT EXIST"

	#retrieve all purchases
	url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(accountId, apiKey)
	r = requests.get(url = url)
	# extracting data in json format
	purchaseData = r.json()

	locationFrequency = {}
	decodedLatLng = {}

	for purchase in purchaseData:
		purchaseInfo = parsePurchase(purchase)
		merchantId = purchaseInfo["merchantId"]
		merchantInfo = parseMerchant(merchantId)
		lat = merchantInfo["lat"]
		lng = merchantInfo["lng"]

		code = geohash2.encode(lat, lng)
		code = code[:-8]

		if code in locationFrequency:
			locationFrequency[code] += 1
			decodedLatLng[geohash2.decode(code)] += 1
		else:
			locationFrequency[code] = 1
			decodedLatLng[geohash2.decode(code)] = 1

	out = sorted(decodedLatLng, reverse=True, key=decodedLatLng.get)
	locations = out[0:5]

	outputData = parseGroupon(locations)
	return (str(outputData))
	#return json.dumps(purchaseData)

def parsePurchase(purchase):
	merchantId = purchase["merchant_id"]
	amountSpent = purchase["amount"]
	return {"merchantId": merchantId, "amountSpent": amountSpent}

def parseMerchant(merchantId):
	url = 'http://api.reimaginebanking.com/merchants/{}/?key={}'.format(merchantId, apiKey)
	r = requests.get(url = url)
	# extracting data in json format
	merchantData = r.json()

	merchantName = merchantData["name"]
	merchantLatLng = merchantData["geocode"]
	merchantCategory = merchantData["category"]
	merchantInfo = {"name": merchantName, "lat": merchantLatLng["lat"],
	 "lng": merchantLatLng["lng"], "category": merchantCategory}
	return merchantInfo

def retrieveGroupon(jsonData):
	output = []
	#print (str(jsonData))
	for i in range(5):
		out = {}
		try:
			out['title'] = jsonData['deals'][i]['title']
		except:
			return None
		rawUrl = jsonData['deals'][i]['dealUrl']
		intermediate = rawUrl[109:]
		out['url'] = 'https://www.groupon.com/deals/' + intermediate[:-123]
		out['image'] = jsonData['deals'][i]['grid4ImageUrl']
		out['discountP'] = jsonData['deals'][i]['options'][0]['discountPercent']
		output.append(out)
	return output

def parseGroupon(locations):
	outputData = {'electronicsData':[], 'foodAndDrinkData':[],
	'funData': [], 'clothingData':[], 'essentialsData':[],
	'healthData':[], 'otherData': []}

	loc = locations[0]
	#Electronics Data
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:electronics&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	electronicsData = r.json()
	#print (electronicsData['deals'])
	#print (str(electronicsData))
	outputData['electronicsData'].append(retrieveGroupon(electronicsData))

	#Food and Drink
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:food-and-drink&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	foodAndDrinkData = r.json()
	outputData['foodAndDrinkData'].append(retrieveGroupon(foodAndDrinkData))

	#Fun
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:entertainment-and-media&filters=category:beauty-and-spas&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	funData = r.json()
	outputData['funData'].append(retrieveGroupon(funData))

	#Clothing
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:retail&filters=category:mens-clothing-shoes-and-accessories&filters=category:womens-clothing-shoes-and-accessories&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	clothingData = r.json()
	outputData['clothingData'].append(retrieveGroupon(clothingData))

	#Essentials
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:for-the-home&filters=category:groceries-household-and-pets&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	essentialsData = r.json()
	outputData['essentialsData'].append(retrieveGroupon(essentialsData))

	#Health
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:health-and-fitness&filters=category:health-and-beauty&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	healthData = r.json()		
	outputData['healthData'].append(retrieveGroupon(healthData))

	#Other
	url = 'https://partner-api.groupon.com/deals.json?tsToken=UK_AFF_0_211827_212556_0&lat={}&lng={}&radius:20&filters=category:automotive&filters=category:tour-travel&offset=0&limit=5'.format(loc[0], loc[1])
	r = requests.get(url = url)
	# extracting data in json format
	otherData = r.json()
	outputData['otherData'].append(retrieveGroupon(otherData))

	return outputData


if __name__ == "__main__":
    app.run()
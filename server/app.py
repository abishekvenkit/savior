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
geocodeAPIKEY = 'AIzaSyAZl193a7iWy35ZAdhU1bjXj0VE-mqW85o'
email = 'abishekvenkit@gmail.com'


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
	# try:
	# 	decodedToken = auth.verify_id_token(idToken)
	# except:
	# 	return "INVALID USER TOKEN"
	# uid = decodedToken['uid']

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

	for purchase in purchaseData:
		purchaseInfo = parsePurchase(purchase)
		merchantId = purchaseInfo["merchantId"]
		merchantInfo = parseMerchant(merchantId)
		lat = merchantInfo["lat"]
		lng = merchantInfo["lng"]

		code = geohash2.encode(lat, lng)
		code = code[:-4]
		if code in locationFrequency:
			locationFrequency[code] += 1
		else:
			locationFrequency[code] = 1

	return str(locationFrequency)

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


if __name__ == "__main__":
    app.run()
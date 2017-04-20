#!/usr/bin/env python3
import requests, json, sys, csv
from config import *

# Set API url variable for processing based on argument passed when script executed; exit if no or incorrect argument passed
if len(sys.argv) > 1:
	apiUrl = str(sys.argv[1])

	if apiUrl.find("/resources/productStyle/v1/") > 0:

		if APP_ID:
			myHeader = {"appId": APP_ID,
						"User-Agent": "Work with productStyle Python Script",
						"From": CONTACT
						}
			apiUrl = apiUrl + "?isEffectiveDateAware=false&appId=" + APP_ID	#Append appId and another parameter to API call

		else:
			print("Local config file not found - cannot proceed")
			sys.exit(2)

	else:
		print("Invalid argument -- submit a valid productStyle API URL to proceed")
		sys.exit(2)
else:
	print("No argument found -- submit a productStyle API URL to proceed")
	sys.exit(2)

######################################### FUNCTION DEFINITIONS #########################################

# Function that iterates through a productStyle API response and works with the data differently depending on the format of the JSON
def processColors(productStyleVariantList, output):

	# Figure out if the initial node of the product data graph is in a list or a dictionary and work through the json response accordingly
	# If the initial node is a dictionary object type, there is only one variant present and does not need to be looped through
	if type(productStyleVariantList) is dict:

		# Print variant info to console and log to .csv
		print("Single variant: {0}".format(productStyleVariantList['variantName']))
		output.writerow(["Only one variant in the response"])
		output.writerow([productStyleVariantList['variantName']])

		# Check if there is a list of colors or just a single color, represented in the response as the presence of a dictionary object
		if type(productStyleVariantList['productStyleColors']) is list:

			print("Multiple colors within the lone variant")
			output.writerow(["Multiple colors within the lone variant"])

			# Iterate through each style color in the list
			for colors in productStyleVariantList['productStyleColors']:

				# Print color info to console and log to .csv
				print(colors['businessCatalogItemId'])
				output.writerow([colors['businessCatalogItemId']])

				'''
				Iterate through style color data elements and child SKUs in order to accomplish your task
				'''

		# If there is only a single color, do not loop but grab the data from the dictionary via keys
		elif type(productStyleVariantList['productStyleColors']) is dict:

			print("One color within the lone variant")
			output.writerow(["One color within the lone variant"])

			# Print color info to console and log to .csv
			print(productStyleVariantList['productStyleColors']['businessCatalogItemId'])
			output.writerow(productStyleVariantList['productStyleColors']['businessCatalogItemId'])

			'''
			Work with single style color's data elements and child SKUs in order to accomplish your task
			'''

	# If there are multiple variants in the response, iterate through each one and access the colors nested within
	elif type(productStyleVariantList) is list:

		print("Multiple variants in the response")
		output.writerow(["Multiple variants in the response"])

		for variant in productStyleVariantList:		# Iterate through each variant

			# Print variant info to console and log to .csv
			print(variant['variantName'])
			output.writerow([variant['variantName']])

			# Check if there is a list of colors or just a single color, represented in the response as the presence of a dictionary object
			if type(variant['productStyleColors']) is list:

				print("Multiple colors in the variant")
				output.writerow(["Multiple colors in the variant"])

				for x in range(len(variant['productStyleColors'])):	# Iterate through each color in the variant

					# Print color info to console and log to .csv
					print(variant['productStyleColors'][x]['businessCatalogItemId'])
					output.writerow([variant['productStyleColors'][x]['businessCatalogItemId']])

					'''
					Iterate through style color data elements and child SKUs in order to accomplish your task
					'''

			# If there is only a single color, do not loop but grab the data from the dictionary via keys
			elif type(variant['productStyleColors']) is dict:

				print("One color in the variant")
				output.writerow(["One color in the variant"])

				# Print color info to console and log to .csv
				print(variant['productStyleColors']['businessCatalogItemId'])
				output.writerow([variant['productStyleColors']['businessCatalogItemId']])

				'''
				Work with single style color's data elements and child SKUs in order to accomplish your task
				'''

	return

# Function that makes API request until successful response obtained, returns that response for processing
def apiRequest(url):

	try:

		apiResponse = requests.get(url, headers=myHeader)
		apiResponse.close()
		apiStatusCode = apiResponse.status_code
		x = 0

	except requests.exceptions.ConnectionError as e:

		apiResponse = ""
		apiStatusCode = 0
		x = 21

	# Make sure initial request is successful; if not, re-request until successful response obtained with max of 20 attempts
	while (apiStatusCode != 200 and apiStatusCode != 204 and x < 20):
		print(url, " - ", apiStatusCode, ": ", apiResponse.elapsed)
		apiResponse = requests.get(url, headers=myHeader)
		apiResponse.close()
		apiStatusCode = apiResponse.status_code
		x += 1

	return apiResponse, apiStatusCode

######################################### END OF FUNCTION DEFINITIONS #########################################

# Prepare output file, write header row
csvfile = open ("color-info.csv", "w")
reportwriter = csv.writer(csvfile)

# Make productStyle API request, put response and status code into variables
response = apiRequest(apiUrl)
productResponse = response[0]
statusCode = response[1]

# Try to convert the response to a JSON object
try:
	productResponse = productResponse.json()
	jsonObject = True

except (ValueError, AttributeError) as e:
	jsonObject = False

# Check API response status code and proceed if it indicates 'success' and valid API JSON response was returned
if statusCode == 200 and jsonObject:

	resource = productResponse["resourceUrl"]	# Grab API request URL
	print("API call is: {0}".format(resource))	# Log request URL to the console
	reportwriter.writerow([resource])			# Log request URL to the output file

	# Process API response
	processColors(productResponse["productStyleV1"]["productStyleVariantList"], reportwriter)

else:

	print("Bad API request - try again with a different URL or product ID")

csvfile.close()		# Close output file

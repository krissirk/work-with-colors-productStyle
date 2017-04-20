import requests, json, time, sys, csv
from config import *

# Set variables for processing based on argument passed when script executed; exit if no or incorrect argument passed
if len(sys.argv) > 1:
	apiUrl = str(sys.argv[1])

	if apiUrl.find("/resources/productStyle/v1/") > 0:
		myHeader = {"appId": APP_ID,
					"User-Agent": "Work with productStyle Python Script",
					"From": CONTACT
					}
	else:
		print("Invalid argument -- submit a valid productStyle API URL to proceed")
		sys.exit(2)
else:
	print("No argument found -- submit a productStyle API URL to proceed")
	sys.exit(2)

######################################### FUNCTION DEFINITIONS #########################################

# Function that iterates through a productStyle API response and works with the data differently depending on the format of the JSON
def processColors(productStyleVariantList, output):

	# Figure out if the colors graph is in a list or a dictionary and work through the json response accordingly
	if type(productStyleVariantList) is dict:

		for colors in productStyleVariantList['productStyleColors']:	# Iterate through each style color in the response

			# Print color info to console
			print(productStyleVariantList['variantName'])
			print(colors['businessCatalogItemId'])

			# Log color info to a .csv
			output.writerow([productStyleVariantList['variantName']])
			output.writerow([colors['businessCatalogItemId']])

	elif type(productStyleVariantList) is list:

		for variant in productStyleVariantList:		# Iterate through each variant in the response

			# Print variant info to console and log to .csv
			print(variant['variantName'])
			output.writerow([variant['variantName']])

			for x in range(len(variant['productStyleColors'])):	# Iterate through each color in the variant

				# Print color info to console and log to .csv
				print(variant['productStyleColors'][x]['businessCatalogItemId'])
				output.writerow([variant['productStyleColors'][x]['businessCatalogItemId']])

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

	# Make sure initial request is successful; if not, re-request until successful response obtained
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
reportwriter.writerow(["variantNames-and-colorIds"])

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

	# Process API response
	processColors(productResponse["productStyleV1"]["productStyleVariantList"], reportwriter)

else:

	print("Bad API request - try again with a different URL or product ID")

csvfile.close()		# Close output file

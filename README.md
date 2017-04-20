This Python script helps clients of Gap Inc.'s productStyle API work with different nuances of the response and data graph resulting in different types of products in the catalog being requested.

Execute the script by passing a properly formatted productStyle API request URL with a valid style or style color number. The complete list of size variant and style color ID data in the complete product graph will be logged to the console and written to a local .csv file.

Inspect the code to learn more about various data scenarios that must be considered when using the productStyle API to consume Gap Inc. product data.

Make sure a config.py file with personalized values for the variables exists in the same directory when executing the script.

I had fun with adding try/except and if/else error handling throughout this script to catch the various input and product data scenarios that one might encounter executing this script.

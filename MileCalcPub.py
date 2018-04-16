'''

This Script is for calcuting distance and payments for KinderKonzert serives at the Portland Symphony Orchestra

'''

# This libraries are specifically for Pythonista on iOS
import dialogs
import console
import clipboard
# These libraries work more in more common environments 
import requests
import json	

# Clear the console and set fonts to default 
console.clear()
console.set_font()

# Get the address from the clipboard
destination = clipboard.get()
totalMusicianCosts = []

# Set the filename for the csv output file 
askForFileName = input('What would you like to name the csv file?')
fileName = askForFileName + '.csv'


# Functions
def writeToFile(line):
	with open(fileName, 'a') as out:		
		out.write(line + '\n')

# A conditional statement that takes the selected menu item and returns a library of musicians 
menuChoices = 'Woodwinds', 'Strings', 'Brass', 'Percussion'
group = dialogs.list_dialog(title='Which Group?', items=menuChoices, multiple=False)

if group == 'Woodwinds':
	ensemble = {
	'Tom Pinkham':'133 Coyle Street Portland ME 04103', 
	'Kristin Trip':'133 Coyle Street Portland ME 04103', 
	'Stephen Birk':'1330 Whig Hill Road Stafford, NH 03884', 
	'Jane Paul':'20 Laurel Lane Durham, NH 03824', 
	'Lauren Spring': '61 Massachusetts Ave Dedham, MA 02026',
	'Matthew Berger':'88 Pitt Street South Portland, ME 04106' 
	}
elif group == 'Brass':
	ensemble = {
		'Dana Pine':'10 Symmes Street Roslindale, MA 02131',
		'Bethany Orange':'29 Walnut Crest Road Gorham, ME 04038',
		'Lauren Spring': '61 Massachusetts Ave Dedham, MA 02026',
		'Bob Haute':'31 Symphony Road Boston MA 02115', 
		'Donald Rink':'13 Spring Valley Road Medfield, MA 02052',
		'Matthew Berger':'88 Pitt Street South Portland, ME 04106'
	}
elif group == 'Strings':
	ensemble = {
		'Lauren Johnson':'418 Goodwin Road Carthage ME 04224',
		'Mina Lavcheva':'27 Kilsyth Road Medford MA 02115',
		'Denise Ortley':'70 Ward Rd Windham ME 04062',
		'Jim Banes':'257 Halls Pond Road South Paris ME 04281',
		'Joe Bronson':'76 Standish Road Watertwon MA 02472'
 	}
elif group == 'Percussion':
	ensemble = {
		'Nancy Sika':'25 Grand Street South Portland, ME 04106',
		'Greg Diamond':'51 Norfolk Street Roxbury, MA 02119',
		'John Worth':'186 Beech Hill Road Rockport, ME 04856'
	}
	
# A menu for choosing the per diem
perDiemChoices = 'Breakfast', 'Lunch', 'Dinner'
perDiem = dialogs.list_dialog(title='Which Per Diem?', items=perDiemChoices, multiple=False)

if perDiem == 'Breakfast':
	perDiemPay = 6.75
elif perDiem == 'Lunch':
	perDiemPay = 9.45
elif perDiem == 'Dinner':
	perDiemPay = 10.45


# Print the destination 
print('Destination:') 
print(destination)
print('----------------------------------', '\n')  

# Write top row names to CSV file
writeToFile('Name' + ',' + 'Wages' + ',' +'Per Diem' + ',' + 'Mileage')

# A for-loop that takes each key (musician) and grabs their address and GET's the address to Google Maps
for musician, home in ensemble.items():
	apiCall = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin= '+home+'&destination='+destination+'&key=AIzaSyBgugX7rBmdqDLCL3zMKkmO7LzIVIA-Vo8')

# This section parses out the JSON to get the musicians mileage
	payload = apiCall.text
	payloadDic = json.loads(payload)
	mileageString = payloadDic['routes'][0]['legs'][0]['distance']['text']
	
# Parsing and setting the Musician Leader wages
	if musician == 'Tom Pinkham' or musician == 'Dana Pine' or musician == 'Lauren Johnson' or musician == 'Nancy Sika':
		musicianWages = 151.50 + 50
	else:
		musicianWages = 151.50
			
# This section calculates roundtrip mileage, reimbursement, and total on the check.  
	mileageInt = float(mileageString.split()[0])
	totalRoundTrip = mileageInt * 2
	mileagePay = totalRoundTrip * .3
	totalPayVoucher = "{0:.2f}".format(musicianWages + perDiemPay + mileagePay)
	totalMusicianCosts.append(float("{0:.6}".format(totalPayVoucher)))
	
# Writing the results to the CSV File
	writeToFile(musician + ', ' + "{0:.2f}".format(musicianWages) + ', ' + "{0:.2f}".format(perDiemPay) + ', ' + "{0:.2f}".format(mileagePay))

# Printing the results	
	console.set_font('Avenir', 16)
	print(musician, ':', home)
	print('Miles: ' + "{0:.1f}".format(totalRoundTrip))
	print('Wages: $'+"{0:.2f}".format(musicianWages))
	print('Mileage: $' + "{0:.2f}".format(mileagePay))
	print('Per Diem: $' + "{0:.2f}".format(float(perDiemPay)))
	print('Total Pay Voucher: $' + totalPayVoucher + '\n')

console.set_font('Avenir', 20)		
print('_'*33)
print('Total Cost of Performance: $' + "{0:.2f}".format(sum(totalMusicianCosts)))

# Setting the Console back to normal
console.set_font()

#Open the share sheet for sending CSV file to another app
console.open_in(fileName)

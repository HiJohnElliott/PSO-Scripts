'''

This script projects the costs of an entire season of KinderKonzerts at the Portland Symphony Orchetra and produces a CSV file with the pay information for each musician at each venue. 

'''

# Imported Libraries
import requests
import json
import console

# Clear the Console for constitency
console.clear()
console.set_font()

# Global Variables 
getFileName = input('What would you like to name the file?')
fileName = getFileName + '.csv'

# All fucntions that are used 
def writeToFile(line):
	with open(fileName, 'a') as out:		
		out.write(line + '\n')

def getMileage(home, destination):
	apiCall = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin= '+home+'&destination='+destination+'&key=AIzaSyBgugX7rBmdqDLCL3zMKkmO7LzIVIA-Vo8')
	mileageString = json.loads(apiCall.text)['routes'][0]['legs'][0]['distance']['text']
	mileageInt = float(mileageString.split()[0])
	return mileageString, mileageInt

def determineWages(musician):
	if musician == 'Tom Pinkham' or musician == 'Dana Pine' or musician == 'Lauren Johnson' or musician == 'Nancy Sika':
		musicianWages = 151.50 + 50
	else:
		musicianWages = 151.50

# All global variables that end up containing lists or dictionaries 	
runningWages = []	
runningMilesTraveledList = []
runningPerDiem = []
runningMileagePay = []
perDiem = 6.75

# Dictionaires for each ensemble							

woodwinds = {
	'Tom Parchman':'133 Coyle Street Portland ME 04103', 
	'Krysia Tripp':'133 Coyle Street Portland ME 04103', 
	'Stef Burk':'1330 Whig Hill Road Stafford, NH 03884', 
	'Janet Polk':'20 Laurel Lane Durham, NH 03824', 
	'Lauren Winter': '61 Massachusetts Ave Dedham, MA 02026',
	'Matt LaBerge' : '88 Pitt Street South Portland, ME 04106'
}
brass = {
	'Dana Oakes':'10 Symmes Street Roslindale, MA 02131',
	'Betty Rines':'29 Walnut Crest Road Gorham, ME 04038',
	'Lauren Winter':'61 Massachusetts Ave Dedham, MA 02026',
	'Rob Couture' : '31 Symphony Road Boston, MA 02115',
	'Don Rankin':'13 Spring Valley Road Medfield, MA 02052',
	'Matt LeBarge' : '88 Pitt Street South Portland, ME 04106'
}
strings = {
	'Laurie Kennedy':'418 Goodwin Road Carthage ME 04224',
	'Mina Lavcheva':'27 Kilsyth Road Medford MA 02115',
	'Dee Dee Oehrtmann':'70 Ward Rd Windham ME 04062',
	'Jim Kennedy':'257 Halls Pond Road South Paris ME 04281',
	'Joe Holt':'76 Standish Road Watertwon MA 02472'
}
percussion = {
	'Nancy Smith':'25 Grand Street South Portland, ME 04106',
	'Greg Simonds':'51 Norfolk Street Roxbury, MA 02119',
	'John Mehrmann':'186 Beech Hill Road Rockport, ME 04856'
}
	
# A Dictionary that contains the name, address, group, and date for each venue
venues = {
'Brunswick Winds' : ['116 Maquoit Rd Brunswick, ME  04011', woodwinds, 'October 24th 2017'],

'Brunswick Brass' : ['116 Maquoit Rd Brunswick, ME  04011', brass, 'November 13th 2018'],

'Longfellow Elementary' : ['432 Stevens Ave Portland, ME 04103', percussion, 'November 16th 2017'],

'Hall School' : ['23 Orono Rd Portland, ME  04102', woodwinds, 'November 9th 2017'],

'South Portland Performing Arts Center' : ['637 Highland Ave South Portland, ME  04106', brass, 'November 14th 2017'],

'Boothbay' : ['86 Townsend Ave Boothbay Harbor, ME  04538', strings, 'January 9th 2017'],

'Fryeburg Academy Strings' :['745 Main St Fryeburg, ME  04037', strings, 'January 22 2018'],

'Brunswick Strings' : ['116 Maquoit Rd Brunswick, ME  04011', strings, 'February 3rd 2018'],

'Biddeford Performing Arts Center' : ['25 Tiger Way Biddeford, ME 04005', brass, 'February 8 2018'],

'Reiche Community School' : ['166 Brackett St Portland, ME  04102', brass, 'February 14 2018'],

'Village Elementary, York' : ['124 York St York, ME  03909', brass, 'March 1 2018'],

'Lyseth Elementary' : ['175 Auburn St Portland, ME  04103', brass, 'March 7 2018'],

'Ocean Avenue School' : ['150 Ocean Avenue Porltand, ME 04103', brass, 'March 9 2018'],

'Presumpscot Elementary' : ['69 Presumpscot St Portland, ME  04103', brass, 'March 22 2018'],

'Cape Elizabeth' : ['12 Scott Dyer Rd Cape Elizabeth, ME', woodwinds, 'March 27 2018'],

'Windham High School' : ['406 Gray Rd Windham, ME  04062 ', strings, 'March 27 2018'],

'Riverton School' : ['1592 Forest Ave Portland, ME  04103', woodwinds, 'April 26 2018'],

'Olin Arts Center at Bates College Strings' : ['75 Russell St Lewiston, ME 04240', strings, 'May 15 2018'],

'Brunswick Percussion' : ['116 Maquoit Rd Brunswick, ME  04011', percussion, 'May 22nd 2018'],
}

###################################### Logic ######################################################
writeToFile('Date, Event with Musicians, Wages, Mileage, Per Diem')

for key, value in venues.items():
	venueName = key
	address = value[0]
	group = value[1]
	date = value[2]
	print('## ' + venueName + ' - ' + date)
	writeToFile(date + ', ' + venueName)
	# Another for-loop that completes a pay voucher for each musician and appends costs to global variables 
	for musician, home in group.items():
		runningWages.append(determineWages(musician))
		runningPerDiem.append(perDiem)
		localMileagePay = "{0:.2f}".format(getMileage(home, address)[1] * 2 * .3)
		runningMileagePay.append(float(localMileagePay))
		# Write the pay data to the csv file 
		writeToFile(', ' + musician + ', ' + "{0:.2f}".format(determineWages(musician)) + ', ' + "{0:.2f}".format(perDiem) + ', ' + localMileagePay)
		# print the pay data to the console 
		print('**' + musician + '**')
		print('Wages: $', "{0:.2f}".format(determineWages(musician)))
		print('Mileage: $' + str(localMileagePay))
		print('Per Diem: $' + str(perDiem))
		print('\n')
	print('\n')
	writeToFile('\n')

# Printing the final tallies 
console.set_font('Avenir', 16)
print('Total Wages: $' + "{0:.2f}".format(sum(runningWages)))
print('Total Per Diem: $' + "{0:.2f}".format(sum(runningPerDiem)))
print('Total Mileage Compensation: $' + "{0:.2f}".format(sum(runningMileagePay)))
console.set_font('Avenir', 20)
print("{0:.2f}".format(sum(runningMilesTraveledList)),' Miles driven total')
console.set_font('Avenir', 24)
print('Total Cost of all KinderKonzerts: $' + "{0:.2f}".format(sum(runningWages)+ sum(runningPerDiem) + sum(runningMileagePay)))
console.set_font()

# pass the csv file to the share sheet to open elsewhere
console.open_in(fileName)



######################################################################################################
unconfirmedDates = {
'Olin Arts Center at Bates College Winds' : ['75 Russell St Lewiston, ME 04240', woodwinds, 'Date not scheduled'],
'Olin Arts Center at Bates College Percussion' : ['75 Russell St Lewiston, ME 04240', percussion, 'Date not scheduled'],

'Westbrook Performing Arts Center Brass' : ['471 Stroudwater St Westbrook, ME  04092', brass, 'Date not scheduled'],

'Westbrook Performing Arts Center Strings' : ['471 Stroudwater St Westbrook, ME  04092', strings, 'Date not scheduled'],

'Sanford Schools' : ['223 Shaws Ridge Rd Springvale, ME 04073', woodwinds, 'Date not scheduled'],

}

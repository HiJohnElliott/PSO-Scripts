import appex
import csv
import console
import requests
import json

def fileWriter(line):
	with open(newFile, 'a') as out:
		out.write(line + '\n')
		
def getMileage(home, destination):
	apiCall = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin= '+home+'&destination='+destination+'&key=AIzaSyBgugX7rBmdqDLCL3zMKkmO7LzIVIA-Vo8')
	mileageString = json.loads(apiCall.text)['routes'][0]['legs'][0]['distance']['text']
	mileageInt = float(mileageString.split()[0])
	return mileageString, mileageInt
	
filePath = appex.get_file_paths()
newFile = input('What would you like name your clean new file?') + '.csv'
venue = input('What is the address of the venue?')

fileWriter('First Name, Last Name, Group Name, Tix, Phone Number, Email, Distance Traveled')

for file in filePath:
	firstRow = 0
	with open(file) as csvfile:
		file_reader = csv.reader(csvfile)
		for row in file_reader:
			personId = row[0]
			phone = row[1]
			cellPhone = row[2]
			firstName = row[3]
			lastName = row[4]
			orgName = row[5]
			address = row[6]
			city = row[7]
			state = row[8]
			zip = row[9]
			country = row[10]
			personType = row[11]
			tix = row[12]
			useEmail = row[13]
			purchaseDate = row[14]
			comment = row[15]
			dropdownComment = row[16]
			purchaseID = row[17]
			discounts = row[18]
			if firstRow < 1:
				firstRow = firstRow + 1
				pass
			else:
				startingPoint = str(address + ' ' + city + ' ' + state)
				distanceTraveled = str(getMileage(startingPoint, venue)[1])
				print(firstName, lastName, comment, distanceTraveled)
				fileWriter(firstName + ', ' + lastName + ', ' + comment + ', ' + tix + ', ' + phone + ', ' + useEmail + ', ' + distanceTraveled)
			
console.open_in(newFile)


import requests
import appex
import csv
import console
import dialogs
import json


if appex.is_running_extension() == True:
	filePath = appex.get_file_paths()
else:
	filePath = dialogs.pick_document()

destination = input('What is the address of the venue?')

newFile = input('What would you like name your clean new file?') + '.csv'

def fileWriter(line):
	with open(newFile, 'a') as out:
		out.write(line + '\n')


def getMileage(home, destination):
	apiCall = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin= '+home+'&destination='+destination+'&key=AIzaSyBgugX7rBmdqDLCL3zMKkmO7LzIVIA-Vo8')
	try:
		mileageString = json.loads(apiCall.text)['routes'][0]['legs'][0]['distance']['text']
	except:
		mileageString = 'ERROR: Cannot calculate distance'
		mileageInt = 0.0 	
		return mileageString, mileageInt
	else:
		mileageInt = float(mileageString.split()[0])
		return mileageString, mileageInt

fileWriter('First Name, Last Name, Phone, Email, Distance')

with open(filePath) as csvfile:
	file_reader = csv.reader(csvfile)
	for row in file_reader:
			personId, schoolID, SAUName, schoolName, firstName, lastName, title, email, phone, phoneExtension, streetAddress, address2, city, state, zipCode, KinderKonzertGroup = row
			schoolAddress = str(streetAddress) +  ' ' + str(city) +  ', ' +  str(state) +  ' ' +  str(zipCode)
			print(firstName, lastName, schoolName)
			try:
				distanceToVenue = getMileage(destination, schoolAddress)[1]
			except:
				print('ERROR FOR ' + firstName, lastName)
			else:						
				fileWriter(firstName + ', ' + lastName + ', ' + phone + ', ' + email + ', ' + str(distanceToVenue))
	fileWriter('\n')
			

console.open_in(newFile)

import console
import clipboard
import dialogs
import math
from MileageKit import mileageCalc as mk
from kk_groups import groups 

def writeToFile(line):
	with open(filename, 'a') as out:		
		out.write(line + '\n')

def selectType():
	kk_type_choices = 'A', 'B', 'C'
	kk_type = dialogs.list_dialog(title='What type of KinderKonzert is it?', items=kk_type_choices, multiple=False)
	if kk_type == 'A':
		section_pay = 187.52
		leader_pay = 237.52
	elif kk_type == 'B':
		section_pay = 217.52
		leader_pay = 292.52
	elif kk_type == 'C':
		section_pay = 227.52
		leader_pay = 327.52
	return section_pay, leader_pay
	
def selectPD():
	perDiemChoices = 'Breakfast', 'Lunch', 'Dinner'
	perDiem = dialogs.list_dialog(title='Which Per Diem?', items=perDiemChoices, multiple=False)
	if perDiem == 'Breakfast':
		perDiemPay = 6.75
	elif perDiem == 'Lunch':
		perDiemPay = 9.45
	elif perDiem == 'Dinner':
		perDiemPay = 10.45
	return perDiemPay		

def selectMusicians():
	menuChoices = 'Woodwinds', 'Strings', 'Brass', 'Percussion'
	selectGroup = dialogs.list_dialog(title='Which Group?', items=menuChoices, multiple=False)
	ensemble = groups.get(selectGroup)
	ensemble_choices = list(ensemble.keys())
	musicians = dialogs.list_dialog(title='Which musicians?', items=ensemble_choices, multiple=True)
	musicians_dict = {}
	for i in musicians:
		add_ensemble = groups.get(selectGroup)
		musician_address = add_ensemble.get(i)
		add_item = {i : musician_address}
		musicians_dict.update(add_item)
	return musicians_dict
									
																											
########################## Begin Logic ###############################
# Clear and prepare the console
console.clear()
console.set_font('Avenir', 20)

# Set up the output csv file 
askForFilename = input('What would you like the name payroll file?')
filename = askForFilename + '.csv'
writeToFile('Name' + ',' + 'Wages' + ',' + 'Mileage' + ',' + 'Per Diem')
venue = clipboard.get()
print('Venue: ' + venue)
print('----------------------------------', '\n')


# Assign top variables
kk_type = selectType()
perDiem = selectPD()
musicians = selectMusicians()
total = []

for musician, address in musicians.items():
	# Wages
	if musician == 'Tom Parchman' or musician == 'Betty Rines' or musician ==  'Laurie Kennedy' or musician ==  'Greg Simonds':
		wages = kk_type[1]
	else:
		wages = kk_type[0]
	total.append(wages)
	# Mileage
	mileage = mk.roundTripPay(address, venue)
	total.append(mileage)
	# Per Diem
	total.append(perDiem)
	# Write to file
	writeToFile(musician + ', ' + str(wages) + ', ' + str(mileage) + ', ' + str(perDiem))
	# Print to console
	print(musician)
	print('Wages: $' + str(wages))	
	print('Mileage: $' + str(mileage))
	print('Per Diem: $' + str(perDiem), '\n')
console.set_font('Avenir', 25)
print('Total pay: $' + (str("{0:.2f}".format(math.fsum(total)))))

console.clear()
print('Where would you like to open the payroll file?')
console.set_font()
console.open_in(filename)

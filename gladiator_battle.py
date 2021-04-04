#built-in random integer generator for dice mechanics
from random import randint	

#LXML library for parsing and writing XML data
from lxml import etree	

#clear the command line
import os
os.system('clear')

#===========================================================================
#functions
#===========================================================================
def roll_dice(faces, quantity, option):
#this function rolls dice
#it takes the number of faces, quantity, and scenario option (such as advantage) and outputs the roll result

	#initializes values
	roll_sum = 0
	roll_count = 1
	dual_roll = []

	#this is the dictionary of possible dice rolls
	dice_dict = {
	'd4' : 4,
	'd6' : 6,
	'd8' : 8,
	'd10' : 10,
	'd12' : 12,
	'd20' : 20,
	'd100' : 100
	}

	if option == 'sum':
		#a while loop is run a number of times equal to input quantity and is summed each time
		while roll_count < quantity + 1:
			#the code corelates the string value to the quantity then generates a random integer
			roll_sum = roll_sum + randint(1, dice_dict[faces])
			#increment the roll counter
			roll_count += 1

		#function is complete and outputs the sum of the rolls
		return roll_sum
	
	elif option == 'adv' or option == 'dis':
		#this will likely ever only be used with a d20, but other dice may be used without limitation
		#this chunk ignores whatever quantity is input because advantage/disadvantage die are only rolled twice
		dual_roll.append(randint(1, dice_dict[faces]))
		dual_roll.append(randint(1, dice_dict[faces]))
		
		#then return the lowest or highest of the two depending on the 'option' variable
		if option == 'adv':
			return max(dual_roll)
		elif option == 'dis':
			return min(dual_roll)

def display_character_build():
	print(f'\u250f' + '\u2501' * 27 + '\u2513\n' \
		'\u2503' + ' ' * 27 + '\u2503\n' \
		'\u2503' + ' ' * 27 + '\u2503\n' \
		'\u2503' + ' ' * 27 + '\u2503\n' \
		'\u2503' + ' ' * 27 + '\u2503\n' \
		'\u2503' + 'ATR' + '\u2502' + 'RAW' + '\u2502' + 'MOD' + ' ' * 2 + 'HP' + '\u2502' + 'AC' + '\u2502' + 'SP' + ' ' * 6 + '\u2503\n' \
		'\u2503' + '\u2500' * 3 + '\u253c' + '\u2500' * 3 + '\u253c' + '\u2500' * 3  + ' ' * 2 + '\u2500' * 2 + '\u253c' + '\u2500' * 2 + '\u253c' + '\u2500' * 2  + ' ' * 6 + '\u2503\n' \
		'\u2503' + ' ' * 3 + '\u2502' + ' ' * 3 + '\u2502' + ' ' * 7 + '\u2502' + ' ' * 2 + '\u2502' + ' ' * 8 + '\u2503\n' \
		'\u2503' + ' ' * 3 + '\u2502' + ' ' * 3 + '\u2502' + ' ' * 19 + '\u2503\n' \
		'\u2503' + ' ' * 3 + '\u2502' + ' ' * 3 + '\u2502' + ' ' * 5 + 'WEAPONS/ARMOR' + ' ' + '\u2503\n' \
		'\u2503' + ' ' * 3 + '\u2502' + ' ' * 3 + '\u2502' + ' ' * 19 + '\u2503\n' \
		'\u2503' + ' ' * 3 + '\u2502' + ' ' * 3 + '\u2502' + ' ' * 19 + '\u2503\n' \
		'\u2503' + ' ' * 3 + '\u2502' + ' ' * 3 + '\u2502' + ' ' * 19 + '\u2503\n' \
		'\u2503' + ' ' * 27 + '\u2503\n' \
		'\u2517' + '\u2501' * 27 + '\u251b')

def build_character():
	#start building the XML by declaring the root node
	root = etree.Element('root')

	#create a node under root that contains character data
	character_branch = etree.SubElement(root, 'character')

	#-----CHARACTER INFO-----#
	#name length validation loop
	selection_status = False
	while selection_status == False:	

		char_name = input('Name your gladiator: ')
		selection_status = validate_string_length(char_name, 25)

	#establish and write to the name tag
	name_branch = etree.SubElement(character_branch, 'name')
	name_branch.text = char_name

	#establish the race tag, call the list selector function, then write the selection
	race_branch = etree.SubElement(character_branch, 'race')
	tag_name = list_selection('race_data.xml', 'name')
	etree.SubElement(race_branch, tag_name)

	#-----INVENTORY-----#
	#establish the inventory tag, call the list selector function, then write the selection
	inventory_branch = etree.SubElement(root, 'inventory')
	tag_name = list_selection('weapon_data.xml', 'name')
	etree.SubElement(inventory_branch, tag_name)

	#-----SAVE DATABASE-----#
	#once character building is complete the XML file is written
	et = etree.ElementTree(root)
	et.write('character_data.xml', pretty_print=True)		

def validate_selection(player_selection, upper_limit):
	#validation statuses are assumed to be False unless proven to be True
	validation_status = [False, False]

	#checks if the value is numeric
	if player_selection.isdigit() == True:
		player_selection = int(player_selection)
		validation_status[0] = True
	elif player_selection.isdigit() == False:
		print('Error: input was not numeric')
		validation_status[0] = False
		return False

	if validation_status[0] == True and player_selection > 0  and player_selection <= upper_limit:
		validation_status[1] = True
	elif player_selection <= 0 or player_selection > upper_limit:
		print('Error: input was out of range')
		validation_status[1] = False
		return False

	#final validation check
	if all(validation_status) == True:
		return True

def validate_string_length(player_selection, char_limit):
	#validation status is assumed to be False unless proven to be true
	validation_status = False

	#checks if the character length exceeds the character limit
	if len(player_selection) > char_limit: 
		validation_status = False
		print(f'Error: input must be less than {char_limit} characters long')
		return False
	elif len(player_selection) <= char_limit:
		return True

def list_selection(data_list, tag_name):
#this function prints a list of elements that exist in an XML file
#the function receives the name of the data file and the tag that will be searched
#the function returns the parent of the node that matches the tag_name input	

	selection_list = []
	list_number = 1

	#this essentially imports the data (i.e. parses it)
	tree = etree.parse(data_list)
	
	#this establishes the root node of the XML database
	root = tree.getroot()

	#begin the list printing
	print('Choose from the following: ')
	
	#this loop iterates through XML database and searches for the specified tag name
	#it stores the tags of the first-level data in a list
	for child in root.iter(tag_name):
		selection_list.append(child.text)
		print(f'{list_number}. {child.text}')
		list_number += 1

	#selection validation loop
	selection_status = False
	while selection_status == False:	

		list_selection = input('Player selection: ')
		selection_status = validate_selection(list_selection, len(selection_list))

	#this is an lxml data type
	tag_name = root[int(list_selection) - 1]
	return tag_name.tag

#===========================================================================
#game loop
#===========================================================================
#tbd
#===========================================================================
#testing
#===========================================================================
# this tests the functionality of the character building function
# running this should write the player inputs to the character_xml data file
# used continually to test the function of the code as development progresses 
build_character()

# #this tests the printout of the character stats and information
# #used as-needed to generate a reference image
# display_character_build()

# #this tests the functionality of the user-input validation function
# #the function should behave similarly to the other selection validation function
# #it should return True or False
# #should be False
# validate_string_length('qwertyuiopasdfghjklzx', 20)
# #should be True
# validate_string_length('qwertyuiopasdfghjklz', 20)

# #this tests the functionality of the numeric input validation function
# #the function receives a numeric input 
# #then assesses if it's greater than zero and less than or equal to the limit
# #should be True
# validate_selection('1',2)
# #should be True
# validate_selection('2',2)
# #should be False
# validate_selection('3',2)
# #should be False
# validate_selection('0',2)
# #this should be False
# validate_selection('A',1)

# #this tests the functionality of the list printing functiong
# #running this should print the items of an XML file as a list
# #the user should be prompted for an input that corresponds to the list
# #the function returns the tag name of a node
# list_selection('weapon_data.xml', 'name')

# # this tests the function of a die roller
# # it takes an input of a string value corresponding to the number of faces of a die
# # it also takes the quantity of dice
# # the function then determine if the player needs advantgage, disadvantage, or the sum
# # it returns the roll or sum of the rolls if multiple dice are used
# print(roll_dice('d20', 2, 'adv'))
# print(roll_dice('d20', 2, 'dis'))
# print(roll_dice('d100', 1, 'sum'))

#STATIC_DEPS=true sudo pip install lxml
#pip install requests
from lxml import html
import requests
import json
from collections import OrderedDict
from parseRecipe import parseRecipe
from transformation import transformRecipe


link = raw_input('Copy an allrecipes link here\n')
parseRecipe(link)

print "1. Lactose-free"
print "2. Vegetarian"
print "3. Low-carb"
print "4. Low-fat" 
print "5. Pescatarian"
print "6. Bake to stir-fry"
n = 10
while n > 0:
	choice = raw_input('Select a transformation by number\n')
	if choice is "1":
		transformRecipe('lactose-free')
	elif choice is "2":
		transformRecipe('vegetarian')
	elif choice is "3": 
		transformRecipe('low-carb')
	elif choice is "4": 
		transformRecipe('low-fat')
	else:
		transformRecipe('pescatarian')

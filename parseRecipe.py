#STATIC_DEPS=true sudo pip install lxml
#pip install requests
from lxml import html
import requests
import json
from collections import OrderedDict

def parseRecipe(link):
	page = requests.get(link)
	tree = html.fromstring(page.text)

	servings = tree.xpath('//span[@id="lblYield"]/text()')
	ingr_amount = tree.xpath('//span[@class="ingredient-amount"]/text()')
	ingr_name = tree.xpath('//span[@class="ingredient-name"]/text()')
	dirs = tree.xpath('//span[@class="plaincharacterwrap break"]/text()')

	# print "Servings: " , servings
	# print "Amount: ", ingr_amount
	# print "Ingredient: ", ingr_name
	# print "Directions: " , dirs

	ingredients = []
	offset = 0
	#pair up the ingredients and amounts
	for i in range(0, len(ingr_name)):
		ing = {}
		ing['name'] = ingr_name[i];
		if "to taste" in ingr_name[i]: 
			offset+=1
			ing['quantity'] = "to taste"
			ing['measurement'] = "N/A"
			print "offset"
		else: 
			quantity = ingr_amount[i-offset].split()
			if len(quantity) is 1: 
				ing['quantity'] = quantity[0]
				ing['measurement'] = "pieces"
			else:
				ing['quantity'] = quantity[0]
				ing['measurement'] = quantity[1]
		ingredients.append(ing);

	tools= []
	primary_methods =[]
	all_methods = []

	directions = []
	for direction in dirs: 

		tool_list = open('tools.txt','r')
		for tool in tool_list:
			tool = tool.rstrip()
			if tool.lower() in direction.lower(): 
				tools.append(tool);

		primary_list = open('primaryCookingMethods.txt','r')
		for primary in primary_list:
			primary = primary.rstrip()
			if primary.lower() in direction.lower(): 
				primary_methods.append(primary);

		all_list = open('allCookingMethods.txt','r')
		for method in all_list:
			method = method.rstrip()
			if method.lower() in direction.lower(): 
				all_methods.append(method);


		directions+=direction.split('. ')


	recipe = {}
	recipe['ingredients'] = ingredients
	recipe['directions'] = directions
	recipe['servings'] = servings
	recipe['tools'] = tools
	recipe['primary cooking methods'] = primary_methods
	recipe['all cooking methods'] = all_methods

	with open('recipe.json', 'w') as outfile:
		    json.dump(OrderedDict(recipe), outfile)
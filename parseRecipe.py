#STATIC_DEPS=true sudo pip install lxml
#pip install requests
from lxml import html
import requests
import json
from collections import OrderedDict


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def most_common(lst):
    return max(set(lst), key=lst.count)

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
			#print "offset"
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


		directions.append(direction.split('. '))


	recipe = {}
	recipe['url'] = link
	recipe['ingredients'] = ingredients
	recipe['directions'] = directions
	recipe['servings'] = servings
	recipe['cooking tools'] = remove_duplicates(tools)
	recipe['primary cooking method'] = most_common(primary_methods)
	recipe['cooking methods'] = remove_duplicates(all_methods)

	with open('Recipes/recipe.json', 'w') as outfile:
		    json.dump(OrderedDict(recipe), outfile)

	return recipe
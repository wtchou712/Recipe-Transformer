#STATIC_DEPS=true sudo pip install lxml
#pip install requests
from lxml import html
import requests
import json
from collections import OrderedDict

#function for removing duplicates
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

#function for finding most common item in an array
def most_common(lst):
    return max(set(lst), key=lst.count)

def parseRecipe(link):
	#get the html from the inputted link
	page = requests.get(link)
	tree = html.fromstring(page.text)

	#using specific ids and classes, store the strings in those ids and classes into an array
	servings = tree.xpath('//span[@id="lblYield"]/text()')
	ingr_amount = tree.xpath('//span[@class="ingredient-amount"]/text()')
	ingr_name = tree.xpath('//span[@class="ingredient-name"]/text()')
	dirs = tree.xpath('//span[@class="plaincharacterwrap break"]/text()')

	#remove any instances of u'\xa0' from html
	ingr_nameCopy =[]
	for i in range(0, len(ingr_name)):
		if ingr_name[i]!= u'\xa0':
			ingr_nameCopy.append(ingr_name[i])
	ingr_name = ingr_nameCopy

	print ingr_amount
	print len(ingr_amount)
	print ingr_name
	print len(ingr_name)

	ingredients = []
	amount_offset = 0
	name_offset = 0
	#pair up the ingredients and amounts since each ingr_name contains "4 tablespoons"
	#need to split into "4" and "tablespoons"
	for i in range(0, len(ingr_name)):
		ing = {}
		# if ingr_name[i]=="\xa0":
		# 	name_offset+=1
		ing['name'] = ingr_name[i]
		ing['descriptor'] = ""
		ing['preparation'] = ""
		ing['prep-description']=""
		#check specifically for "to taste"
		if "to taste" in ingr_name[i]: 
			amount_offset+=1
			ing['quantity'] = "none"
			ing['measurement'] = "to taste"
		elif "cooking spray" in ingr_name[i]:
			amount_offset+=1
			ing['quantity'] = "none"
			ing['measurement'] = "none"
		
		else: 
			quantity = ingr_amount[i-amount_offset].split()
			#if an ingredient is 4 chicken thighs, the ingredient amoutn will just be 4, not 4 pieces
			if len(quantity) is 1: 
				ing['quantity'] = quantity[0]
				ing['measurement'] = "units"
			else:
				ing['quantity'] = quantity[0]
				ing['measurement'] = quantity[1]
		#store to an array of ingredients
		ingredients.append(ing);

	tools= []
	primary_methods =[]
	all_methods = []
	directions = []
	count =0
	for direction in dirs: 

		#use knowledge base of tools to gather what tools are used in the recipe
		tool_list = open('knowledge-base/tools.txt','r')
		for tool in tool_list:
			tool = tool.rstrip()
			if count == 0: 
				print tool
			if tool in direction.lower(): 
				tools.append(tool);

		#use our knwoledge base of primary cooking methods to gather which primary cooking methods are used in the recipe
		primary_list = open('knowledge-base/primaryCookingMethods.txt','r')
		for primary in primary_list:
			primary = primary.rstrip()
			if primary.lower() in direction.lower(): 
				primary_methods.append(primary);

		#use our knowledge base of cooking methods to gather which cooking methods are used in teh recipe
		all_list = open('knowledge-base/allCookingMethods.txt','r')
		for method in all_list:
			method = method.rstrip()
			if method.lower() in direction.lower(): 
				all_methods.append(method);
		directions.append(direction.split('. '))

		count+=1

	#store the recipe as a json 
	recipe = {}
	recipe['url'] = link
	recipe['ingredients'] = ingredients
	recipe['directions'] = directions
	recipe['servings'] = servings
	recipe['cooking tools'] = remove_duplicates(tools)
	recipe['primary cooking method'] = most_common(primary_methods)
	recipe['cooking methods'] = remove_duplicates(all_methods)

	with open('../parsed-recipes/recipe.json', 'w') as outfile:
		    json.dump(OrderedDict(recipe), outfile)

	return recipe
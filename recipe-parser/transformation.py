import json
from pprint import pprint
from collections import OrderedDict


def transformRecipe(transformType):
	#get the originally parsed recipe
	data = open('../parsed-recipes/recipe.json')
	original = json.load(data)
	data.close()

	newRecipe = {}
	newIngredients = []
	replacedIngredients = {}

	#run through the ingredients in the original recipe
	for ingr in original['ingredients']:
		#get the knowledge base and dictionaries based on the transformation the user wants
		jsontransformation = "knowledge-base/" + transformType + ".json"
		knowledgebase = open(jsontransformation, 'r')
		transformation = json.load(knowledgebase)
		ingredient = {}

		#go through each item in the knowledge base 
		for trans in transformation[transformType]:
			keys = trans.keys()
			for k in keys: 
				#check if any of the ingredients in the knowledge base match the ingredients in the original recipe
				if k in ingr['name'].lower():
					#set the new ingredient to the replacement ingredient
					ingredient['name'] = trans[k]
					break

		#if a new ingredient was not created, then we just copy the original (including measurement and quantity)			
		if ingredient.has_key('name') is False:
			ingredient['name'] = ingr['name']
			ingredient['measurement'] = ingr['measurement']
			ingredient['quantity'] = ingr['quantity']
			ingredient['descriptor'] = []
			ingredient['preparation'] = []
			ingredient['prep-description']=[]

		#else, a new ingredient was created
		else: 
			#now check if we need to change teh measurement from units to pounds
			if ingr['measurement'] == "units": 
				#changes 1 unit to 0.25 pounds i.e. 4 units of chicken would be 1 pound of tofu
				ingredient['measurement'] = "pounds"
				ingredient['quantity'] = str(float(ingr['quantity'])/4)
				ingredient['descriptor'] = ""
				ingredient['preparation'] = ""
				ingredient['prep-description']=""
			else:
				ingredient['measurement'] = ingr['measurement']
				ingredient['quantity'] = ingr['quantity']
				ingredient['descriptor'] = ""
				ingredient['preparation'] = ""
				ingredient['prep-description']=""
		newIngredients.append(ingredient)

	#go through the directions to see what needs to changed
	newDirections = []
	for dirs in original['directions']:
		newSubDirections = [] 
		for subdirs in dirs:
			newDirs = ""

			#get the knowledge base and dictionaries based on the transformation that the user wants
			jsontransformation = "knowledge-base/" +transformType + ".json"
			knowledgebase = open(jsontransformation, 'r')
			transformation = json.load(knowledgebase)

			#go through each item in the knowledge base
			for trans in transformation[transformType]:
				keys = trans.keys()
				for k in keys: 
					#check if one of the ingredients that needs to replaced is in the direction
					if k in subdirs.lower():
						#replace the appropriate ingredient in the direction
						subdirs = subdirs.replace(k, trans[k]) 
						newDirs = subdirs
						break
			#check if a new direction was not set. 
			if newDirs == "":
				#if not, just copy the original direction
				newDirs = subdirs

		#append these directions to the array
			newSubDirections.append(newDirs)
		newDirections.append(newSubDirections)


	#set all the json fields for the new transformed recipe
	newRecipe['directions'] = newDirections
	newRecipe['cooking methods'] = original['cooking methods']
	newRecipe['servings'] = original['servings']
	newRecipe['cooking tools'] = original['cooking tools']
	newRecipe['primary cooking method'] = original['primary cooking method']
	newRecipe['ingredients'] = newIngredients
	newRecipe['url'] = original['url']

	#save the new transformation to the folder of parsed recipes
	with open('../parsed-recipes/recipe-' + transformType + '.json', 'w') as outfile:
		    json.dump(OrderedDict(newRecipe), outfile)

#function for removing duplicates
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

#function for transforming bake to fry
def transformMethod():
	data = open('../parsed-recipes/recipe.json')
	original = json.load(data)
	data.close()

	#swap the preheat oven direction
	directions = original['directions']
	for i in range(0, len(directions)):	
		for j in range(0, len(directions[i])):
			#search for preheat oven direction
			if "preheat the oven" in directions[i][j].lower():
				oldDirection = directions[i][j]
				words = oldDirection.split()
				temperature = int(words[4]) 
				#convert the range of temperature to a stove heat
				heat = ""
				if temperature <= 200: 
					heat = "low"
				elif temperature <= 250: 
					heat = "medium low"
				elif temperature <= 350: 
					heat = "medium"
				elif temperature <= 400:
					heat = "medium-high"
				else:
					heat = "high"
				#create the new direction and the ingredient of oil since we are frying
				newDirection = "Add 2 tablespoons of olive oil to pan and set the stove to " + heat
				newIngredient = {}
				newIngredient['measurement'] = "tablespoons"
				newIngredient['name'] = "olive oil"
				newIngredient['quantity'] = "2"
				newIngredient['descriptor'] = ""
				newIngredient['preparation'] = ""
				newIngredient['prep-description']=""
				
				#replace the old direction wiht the new one
				directions[i][j] = newDirection				
				original['ingredients'].append(newIngredient)
				break

			if "preheat oven" in directions[i][j].lower():
				oldDirection = directions[i][j]
				words = oldDirection.split()
				temperature = int(words[3]) 
				#convert the range of temperature to a stove heat
				heat = ""
				if temperature <= 200: 
					heat = "low"
				elif temperature <= 250: 
					heat = "medium low"
				elif temperature <= 350: 
					heat = "medium"
				elif temperature <= 400:
					heat = "medium-high"
				else:
					heat = "high"
				#create the new direction and the ingredient of oil since we are frying
				newDirection = "Add 2 tablespoons of olive oil to pan and set the stove to " + heat
				newIngredient = {}
				newIngredient['measurement'] = "tablespoons"
				newIngredient['name'] = "olive oil"
				newIngredient['quantity'] = "2"
				newIngredient['descriptor'] = ""
				newIngredient['preparation'] = ""
				newIngredient['prep-description']=""
				
				#replace the old direction wiht the new one
				directions[i][j] = newDirection				
				original['ingredients'].append(newIngredient)
				break

	#search the directions for any of the words: bake, roast, preheated oven, or baking dish
	indexToReplace = []
	for i in range(0, len(directions)):
		for j in range (0, len(directions[i])):
			if "bake" in directions[i][j] or "roast" in directions[i][j] or "preheated oven" in directions[i][j] or "baking dish" in directions[i][j]:
				#store the indices of the direction so we cna replace the appropriate words later on
				indexToReplace.append(i)	

	indexToReplace = remove_duplicates(indexToReplace)
	#now replace the instances of the words 
	for replace_index in indexToReplace:
		for i in range(0, len(directions[replace_index])):
			str1 = directions[replace_index][i]
			str1 = str1.replace("baking", "frying")
			str1 = str1.replace("baked", "fried")
			str1 = str1.replace("bake", "fry")
			str1 = str1.replace("roast", "fry")
			str1 = str1.replace("preheated oven", "frying pan")
			str1 = str1.replace("oven", "frying pan")
			str1 = str1.replace("cooked", "fried")
			str1 = str1.replace("cooking", "frying")
			str1 = str1.replace("cook ", "fry ")
			str1 = str1.replace("Baking", "Frying")
			str1 = str1.replace("Baked", "Fried")
			str1 = str1.replace("Bake", "Fry")
			str1 = str1.replace("Roast", "Fry")
			str1 = str1.replace("Preheated oven", "Frying pan")
			str1 = str1.replace("Oven", "Frying pan")
			str1 = str1.replace("Cooked", "Fried")
			str1 = str1.replace("Cooking", "Frying")
			str1 = str1.replace("Cook", "Fry")
			str1 = str1.replace("baking dish", "frying pan")
			str1 = str1.replace("Baking dish" , "Frying pan")
			str1 = str1.replace("rack", "top of stove")
			#store the newly replaced directions
			directions[replace_index][i] = str1

	#search the directions for any time amounts
	for index in indexToReplace:
		for i in range(0, len(directions[index]	)):
			words = directions[index][i].split()
			for k in range(0, len(words)):
				#check if any contain time amounts such as hour or minutes
				if "hour" in words[k] or "minute" in words[k]: 
					#if "an" is said instead of a number
					if words[k-1] == "an":
						words[k-1] = "12"
						directions[index][i]==""
						#copy over the new directions
						for j in range(0, len(words)):
							directions[index][i]+= words[j] + " "
					else:
						#if we find an integer amount, we divide the number by 5 i.e. 2 hours = 24 min of frying
						words[k-1] = str(float(words[k-1])/5)
						#copy over the new direction 
						directions[index][i] = ""
						for j in range(0, len(words)):
							directions[index][i] += words[j] + " "

	#replace the primary cooking method if it says bake or roast, or just copy original
	primaryMethods = original['primary cooking method']
	newPrimary = ""
	if primaryMethods=="bake":
		newPrimary="pan-fry"
	elif primaryMethods=="roast":
		newPrimary="pan-fry"
	else:
		newPrimary = primaryMethods

	#replace any of the cooking methods if they say bake or roast, or just copy original
	allMethods = original['cooking methods']
	newAll = []
	for method in allMethods:
		#print method
		if method=="bake":
			newAll.append("pan-fry")
		elif method=="roast":
			newAll.append("pan-fry")
		else:
			newAll.append(method)

	#replace any of the tools that are baking dish or oven, or just copy origina1,
	tools = original['cooking tools']
	newTools =[]
	for tool in tools:
		#print tool
		if tool=="baking dish": 
			#print "baking dish match"
			newTools.append("frying pan")
		elif tool=="oven":
			newTools.append("stove")
		else:
			newTools.append(tool)

	#store the new transformed recipe
	recipe = {}
	recipe['ingredients'] = original['ingredients']
	recipe['directions'] = directions
	recipe['servings'] = original['servings']
	recipe['cooking tools'] = remove_duplicates(newTools)
	recipe['primary cooking method'] = newPrimary
	recipe['cooking methods'] = remove_duplicates(newAll)
	recipe['url'] = original['url']
	
	with open('../parsed-recipes/recipe-bake-to-fry.json', 'w') as outfile:
		    json.dump(OrderedDict(recipe), outfile)			











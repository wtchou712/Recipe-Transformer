import json
from pprint import pprint
from collections import OrderedDict


def transformRecipe(transformType):
	data = open('recipe.json')
	original = json.load(data)
	#pprint(original)
	data.close()
	print transformType

	newRecipe = {}
	newIngredients = []
	replacedIngredients = {}
	for ingr in original['ingredients']:
		jsontransformation = transformType + ".json"
		# print jsontransformation
		knowledgebase = open(jsontransformation, 'r')
		transformation = json.load(knowledgebase)
		ingredient = {}
		for trans in transformation[transformType]:
			keys = trans.keys()
			#print keys
			for k in keys: 
				if k in ingr['name'].lower():
					print "match!"
					# print k
					# print trans[k]
					ingredient['name'] = trans[k]
					break
		if ingredient.has_key('name') is False:
			print "nothing found"
			ingredient['name'] = ingr['name']
		if ingr['measurement'] == "pieces": 
			ingredient['measurement'] = "pounds"
			ingredient['quantity'] = str(float(ingr['quantity'])/4);
		else:
			ingredient['measurement'] = ingr['measurement']
			ingredient['quantity'] = ingr['quantity']
		newIngredients.append(ingredient)

	newDirections = []
	for dirs in original['directions']:
		newSubDirections = [] 
		for subdirs in dirs:
			newDirs = ""
			jsontransformation = transformType + ".json"
			# print jsontransformation
			knowledgebase = open(jsontransformation, 'r')
			transformation = json.load(knowledgebase)
			for trans in transformation[transformType]:
				keys = trans.keys()
				#print keys
				for k in keys: 
					if k in subdirs.lower():
						print "direction match!"
						print k
						print subdirs
						print "====================================="
						subdirs = subdirs.replace(k, trans[k]) 
						newDirs = subdirs
						break
			if newDirs == "":
				newDirs = subdirs
			newSubDirections.append(newDirs)
		newDirections.append(newSubDirections)


	newRecipe['directions'] = newDirections
	newRecipe['all cooking methods'] = original['all cooking methods']
	newRecipe['servings'] = original['servings']
	newRecipe['tools'] = original['tools']
	newRecipe['primary cooking methods'] = original['primary cooking methods']
	newRecipe['ingredients'] = newIngredients

	with open('recipe-' + transformType + '.json', 'w') as outfile:
		    json.dump(OrderedDict(newRecipe), outfile)


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

def transformMethod():
	data = open('recipe.json')
	original = json.load(data)
	#pprint(original)
	data.close()

	#swap the preheat oven direction
	directions = original['directions']
	for i in range(0, len(directions)):	
		for j in range(0, len(directions[i])):
			#search for preheat oven direction
			if "preheat the oven" in directions[i][j].lower():
				#print "preheat the oven found"
				oldDirection = directions[i][j]
				words = oldDirection.split()
				temperature = int(words[4]) 
				#print "temperature " + str(temperature)
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
				#create the new direction and the ingredient of oil
				newDirection = "Add 2 tablespoons of olive oil to pan and set the stove to " + heat
				newIngredient = {}
				newIngredient['measurement'] = "tablespoons"
				newIngredient['name'] = "olive oil"
				newIngredient['quantity'] = "2"
				
				#replace the old direction wiht the new one
				directions[i][j] = newDirection
				#print directions[i][j]
				
				original['ingredients'].append(newIngredient)
				# print directions
				# print original['ingredients']
				break
			if "preheat oven" in directions[i][j].lower():
				#print "preheat the oven found"
				oldDirection = directions[i][j]
				words = oldDirection.split()
				temperature = int(words[3]) 
				#print "temperature " + str(temperature)
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
				#create the new direction and the ingredient of oil
				newDirection = "Place the pan on the stove and set to " + heat
				# newIngredient = {}
				# newIngredient['measurement'] = "tablespoons"
				# newIngredient['name'] = "olive oil"
				# newIngredient['quantity'] = "2"
				
				#replace the old direction wiht the new one
				directions[i][j] = newDirection
				#print directions[i][j]
				
				#original['ingredients'].append(newIngredient)
				# print directions
				# print original['ingredients']
				break


	indexToReplace = []
	for i in range(0, len(directions)):
		for j in range (0, len(directions[i])):
			if "bake" in directions[i][j] or "roast" in directions[i][j] or "preheated oven" in directions[i][j] or "baking dish" in directions[i][j]:
				#replace all instances of the words with fry
				indexToReplace.append(i)	

	indexToReplace = remove_duplicates(indexToReplace)
	#print indexToReplace
	#now replace the instances of the words 
	for index in indexToReplace:
		for x in range(0, len(directions[index])):
			#print directions[index][x]
			str1 = directions[index][x]
			str1 = str1.replace("bake", "fry")
			str1 = str1.replace("roast", "fry")
			str1 = str1.replace("preheated oven", "frying pan")
			str1 = str1.replace("oven", "frying pan")
			str1 = str1.replace("cook ", "fry ")
			str1 = str1.replace("Bake", "Fry")
			str1 = str1.replace("Roast", "Fry")
			str1 = str1.replace("Preheated oven", "Frying pan")
			str1 = str1.replace("Oven", "Frying pan")
			str1 = str1.replace("Cook", "Fry")
			str1 = str1.replace("baking dish", "frying pan")
			str1 = str1.replace("Baking dish" , "Frying pan")
			str1 = str1.replace("rack", "top of stove")
			directions[index][x] = str1

	for index in indexToReplace:
		for i in range(0, len(directions[index]	)):
			words = directions[index][i].split()
			for k in range(0, len(words)):
				if "hour" in words[k] or "minute" in words[k]: 
					words[k-1] = str(int(words[k-1])/5)
					#now append the new instruction 
					directions[index][i] = ""
					for j in range(0, len(words)):
						directions[index][i] += words[j] + " "



	#replace the cooking methods and tools
	primaryMethods = original['primary cooking methods']
	newPrimary = ""
	print "primary methods"
	for method in primaryMethods:
		print method
		if method=="bake":
			newPrimary="pan-fry"
		elif method=="roast":
			newPrimary="pan-fry"
		else:
			newPrimary = method

	print "all methods"
	allMethods = original['all cooking methods']
	newAll = []
	for method in allMethods:
		print method
		if method=="bake":
			newAll.append("pan-fry")
		elif method=="roast":
			newAll.append("pan-fry")
		else:
			newAll.append(method)

	tools = original['tools']
	print "tools"
	newTools =[]
	for tool in tools:
		print tool
		if tool=="baking dish": 
			print "baking dish match"
			newTools.append("frying pan")
		elif tool=="oven":
			newTools.append("stove")
		else:
			newTools.append(tool)






	#print directions
	recipe = {}
	recipe['ingredients'] = original['ingredients']
	recipe['directions'] = directions
	recipe['servings'] = original['servings']
	recipe['tools'] = remove_duplicates(newTools)
	recipe['primary cooking methods'] = remove_duplicates(newPrimary)
	recipe['all cooking methods'] = remove_duplicates(newAll)
	
	with open('recipe-bake-to-fry.json', 'w') as outfile:
		    json.dump(OrderedDict(recipe), outfile)			











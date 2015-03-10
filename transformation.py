import json
from pprint import pprint
from collections import OrderedDict

# def toLactoseFree():
# 	data = open('recipe.json')
# 	original = json.load(data)
# 	#pprint(original)
# 	data.close()

# 	newRecipe = {}
# 	newIngredients = []
# 	for ingr in original['ingredients']:
# 		transformation = open('lactose-free.json', 'r')
# 		transformation = json.load(transformation)
# 		ingredient = {}
# 		for trans in transformation["lactose-free"]:
# 			keys = trans.keys()
# 			#print keys
# 			for k in keys: 
# 				if k in ingr['name'].lower():
# 					print "match!"
# 					print k
# 					print trans[k]
# 					ingredient['name'] = trans[k]
# 		if ingredient.has_key('name') is False:
# 			print "nothing found"
# 			ingredient['name'] = ingr['name']
# 		ingredient['measurement'] = ingr['measurement']
# 		ingredient['quantity'] = ingr['quantity']
# 		newIngredients.append(ingredient)

# 	newRecipe['directions'] = original['directions']
# 	newRecipe['all cooking methods'] = original['all cooking methods']
# 	newRecipe['servings'] = original['servings']
# 	newRecipe['tools'] = original['tools']
# 	newRecipe['primary cooking methods'] = original['primary cooking methods']
# 	newRecipe['ingredients'] = newIngredients

# 	with open('recipeLactoseFree.json', 'w') as outfile:
# 		    json.dump(OrderedDict(newRecipe), outfile)

def transformRecipe(transformType):
	data = open('recipe.json')
	original = json.load(data)
	#pprint(original)
	data.close()
	print transformType

	newRecipe = {}
	newIngredients = []
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
		ingredient['measurement'] = ingr['measurement']
		ingredient['quantity'] = ingr['quantity']
		newIngredients.append(ingredient)

	newRecipe['directions'] = original['directions']
	newRecipe['all cooking methods'] = original['all cooking methods']
	newRecipe['servings'] = original['servings']
	newRecipe['tools'] = original['tools']
	newRecipe['primary cooking methods'] = original['primary cooking methods']
	newRecipe['ingredients'] = newIngredients

	with open('recipe-' + transformType + '.json', 'w') as outfile:
		    json.dump(OrderedDict(newRecipe), outfile)




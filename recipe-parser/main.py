#STATIC_DEPS=true sudo pip install lxml
#pip install requests
import Tkinter
from Tkinter import *
import tkMessageBox
from lxml import html
import requests
import json
from collections import OrderedDict
from parseRecipe import parseRecipe
from transformation import transformRecipe
from transformation import transformMethod


##USE THIS CODE IF YOU WANT TO RUN IN TERMINAL INSTEAD OF GUI
# link = raw_input('Copy an allrecipes link here\n')
# parseRecipe(link)
# print "1. Lactose-free"
# print "2. Vegetarian"
# print "3. Low-carb"
# print "4. Low-fat" 
# print "5. Pescatarian"
# print "6. Vegan"
# print "7. Bake to stir-fry"
# n = 10
# while n > 0:
# 	choice = raw_input('Select a transformation by number\n')
# 	if choice is "1":
# 		transformRecipe('lactose-free')
# 	elif choice is "2":
# 		transformRecipe('vegetarian')
# 	elif choice is "3": 
# 		transformRecipe('low-carb')
# 	elif choice is "4": 
# 		transformRecipe('low-fat')
# 	elif choice is "5":
# 		transformRecipe('pescatarian')
# 	elif choice is "6": 
# 		transformRecipe('vegan')
# 	else: 
# 		transformMethod()


top = Tkinter.Tk()
def getSpecificRecipe(phrase):
    if(phrase=="vegetarian"):
        transformRecipe("vegetarian")
        getrec("recipe-vegetarian")
    
    if(phrase=="vegan"):
        transformRecipe("vegan")
        getrec("recipe-vegan")

    if(phrase=="pescatarian"):
        transformRecipe("pescatarian")
        getrec("recipe-pescatarian")

    if(phrase=="low-fat"):
        transformRecipe("low-fat")
        getrec("recipe-low-fat")

    if(phrase=="low-carb"):
        transformRecipe("low-carb")
        getrec("recipe-low-carb")

    if(phrase=="lactose-free"):
        transformRecipe("lactose-free")
        getrec("recipe-lactose-free")

    if(phrase=="baketostir"):
        transformMethod()
        getrec("recipe-bake-to-fry")

    if(phrase=="normal"):
        parseRecipe(input_text.get())
        getrec("recipe");

def getrec(text):
    data = open("../parsed-recipes/"+text+".json")
    original = json.load(data)
    data.close()

    #add the primary cooking method to the textbox that will be on the left of the gui
    primaryCookingMethod=original["primary cooking method"]
    leftInfoColumn = Text(top,width=50,pady=0,wrap=WORD)
    leftInfoColumn.insert(INSERT, "**SCROLLDOWN FOR MORE INGREDIENTS**\n")
    leftInfoColumn.insert(INSERT, "Primary Cooking Method: \n");
    leftInfoColumn.insert(END, primaryCookingMethod+"\n\n");
    leftInfoColumn.grid(row = 2, column = 1, rowspan =12)

    #add the cooking methods to the textbox that will be on the left of the gui
    cookingMethods=original["cooking methods"]
    methodString=""
    for method in cookingMethods:
        methodString= methodString + method + ", "
    methodString = methodString[:-2]
    leftInfoColumn.insert(END, "Cooking Methods: \n");
    leftInfoColumn.insert(END, methodString+"\n\n");

    #add the cooking tools to the textbox that will be on the left of the gui
    cookingTools=original["cooking tools"]
    leftInfoColumn.insert(END, "Tools: \n");
    toolString=""
    for tool in cookingTools:
        toolString= toolString + tool + ", "
    toolString = toolString[:-2]
    leftInfoColumn.insert(END, toolString+"\n\n");

    #add the servings to the textbox that will be on the left of the gui
    servings=original["servings"]
    leftInfoColumn.insert(INSERT, "Servings: \n");

    #add the ingredients to the textbox that will be on the left of the gui
    ingredients=original["ingredients"]
    ingredientString=""
    leftInfoColumn.insert(INSERT, "Ingredients: \n");
    for ingr in ingredients:
        ingredientString= "Name: "+ingr['name']+"\nMeasurement: "+ingr['measurement']+"\nQuantity: " + ingr['quantity']
        leftInfoColumn.insert(END, ingredientString+"\n\n");

    #add the directions to the textbox that will be on the right of the gui
    directions=original["directions"]
    directionString=""
    counter=0
    rightInfoColumn = Text(top,width=50,pady=0,wrap=WORD)
    rightInfoColumn.insert(INSERT, "**SCROLLDOWN FOR MORE DIRECTIONS**\n")
    rightInfoColumn.insert(INSERT, "Directions: \n");
    for dirs in directions:
        for subdirs in dirs:
            counter=counter+1;
            directionString= str(counter)+". "+subdirs
            rightInfoColumn.insert(END, directionString+"\n");
    rightInfoColumn.grid(row = 2, column = 2, rowspan = 12)

#place the input box for the user to enter the recipe url
input_text=StringVar("")
URL_input = Entry(top, bd =1, width=50,textvariable=input_text)
URL_input.grid(row=0,column=1)

#Set the response when the buttons are pressed and the sizes
vegetarianTransBtn = Tkinter.Button(top, text ="Change to Vegetarian",command= lambda: getSpecificRecipe("vegetarian"),width=50, height=2, wraplength=40)
veganTransBtn = Tkinter.Button(top, text ="Change to Vegan",command= lambda: getSpecificRecipe("vegan"),width=50, height=2, wraplength=40)
pescatarianTransBtn= Tkinter.Button(top, text ="Change to Pescatarian",command= lambda: getSpecificRecipe("pescatarian"),width=50, height=2, wraplength=40)
lactoseFreeTransBtn = Tkinter.Button(top, text ="Change to Lactose-free",command= lambda: getSpecificRecipe("lactose-free"),width=50, height=2, wraplength=40)
lowfatTransBtn = Tkinter.Button(top, text ="Change to low fat",command= lambda: getSpecificRecipe("low-fat"),width=50, height=2, wraplength=40)
lowcarbTransBtn = Tkinter.Button(top, text ="Change to low carb",command= lambda: getSpecificRecipe("low-carb") ,width=50, height=2, wraplength=40)
bakeToFryBtn= Tkinter.Button(top, text ="Change from bake to stir fry",command= lambda: getSpecificRecipe("baketostir") ,width=50, height=2, wraplength=40)
parseRecipeBtn = Tkinter.Button(top, text ="Submit Recipe URL",command= lambda: getSpecificRecipe("normal"),width=50, height=2, wraplength=40)

#Set the instructions at the top of the gui for the user
instruction1 = Text(top, width=50, height=1,pady=0)
instruction2 = Text(top, width=50, height=1,pady=0)
instruction1.insert(INSERT, "Enter the URL to get the recipe.")
instruction2.insert(INSERT, "Click a button to transform it.")

#Place all the buttons in the gui grid
instruction1.grid(row=0, column=0)
instruction2.grid(row=1, column=0)
vegetarianTransBtn.grid(row=2,column=0)
veganTransBtn.grid(row=3,column=0)
pescatarianTransBtn.grid(row=4,column=0)
lactoseFreeTransBtn.grid(row=5,column=0)
lowfatTransBtn.grid(row=6,column=0)
lowcarbTransBtn.grid(row=7,column=0)
bakeToFryBtn.grid(row=8,column=0)
parseRecipeBtn.grid(row=0,column=2)

top.mainloop()

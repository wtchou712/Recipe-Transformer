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


def info(phrase):
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
    #tkMessageBox.showinfo( "INFO:", input_text.get())
    data = open("../parsed-recipes/"+text+".json")
    original = json.load(data)
    print(original)
    data.close()
    #pprint(original)
    data=original["primary cooking method"]
    PCM = Text(top,width=40,pady=0,wrap=WORD)
    PCM.insert(INSERT, "Primary Cooking Method: \n");
    PCM.insert(END, data+"\n\n");
    PCM.grid(row = 5, column = 0)
    data=original["cooking methods"]
    metho=""
    for cook in data:
        metho= metho + cook + ", "
    metho = metho[:-2]
    #ACM = Text(top,width=40,pady=0,wrap=WORD)
    PCM.insert(END, "Cooking Methods: \n");
    PCM.insert(END, metho+"\n\n");
    #ACM.grid(row = 5, column = 1)
    data=original["ingredients"]
    #print data
    metho=""
    IN = Text(top,width=40,pady=0,wrap=WORD)
    IN.insert(INSERT, "Ingredients: \n");
    for ing in data:
        #print ing;
        metho= "Name: "+ing['name']+"\nMeasurement: "+ing['measurement']+"\nQuantity: " + ing['quantity']
        IN.insert(END, metho+"\n\n");
    IN.grid(row = 5, column = 1)
    data=original["cooking tools"]
    #Tool = Text(top,width=40,pady=0,wrap=WORD)
    PCM.insert(END, "Tools: \n");
    metho=""
    for cook in data:
        metho= metho + cook + ", "
    metho = metho[:-2]
    PCM.insert(END, metho+"\n\n");
    data=original["servings"]
    PCM.insert(INSERT, "Servings: \n");
    PCM.insert(END, data[0]+"\n\n");
    #PCM.grid(row = 5, column = 0)
    #Tool.grid(row = 6, column = 0)
    data=original["directions"]
    #print data
    metho=""
    counter=0
    Dir = Text(top,width=40,pady=0,wrap=WORD)
    Dir.insert(INSERT, "Directions: \n");
    for dirs in data:
        for subdirs in dirs:
            #print ing;
            counter=counter+1;
            metho= str(counter)+". "+subdirs
            Dir.insert(END, metho+"\n");
    Dir.grid(row = 5, column = 2)



#y= IntVar()
#y.set(2015)  # initializing the choice, i.e. Python


def ShowChoice():
    year= y.get()

input_text=StringVar("")
E1 = Entry(top, bd =1, width = 40,textvariable=input_text)
E1.grid(row=0,column=1)

# Code to add widgets will go here...
Vege = Tkinter.Button(top, text ="Change to Vegetarian",command= lambda: info("vegetarian"),width=40, height=2, wraplength=40)
Vegan = Tkinter.Button(top, text ="Change to Vegan",command= lambda: info("vegan"),width=40, height=2, wraplength=40)
Pesc= Tkinter.Button(top, text ="Change to Pescatarian",command= lambda: info("pescatarian"),width=40, height=2, wraplength=40)
Lact = Tkinter.Button(top, text ="Change to Lactose-free",command= lambda: info("lactose-free"),width=40, height=2, wraplength=40)
Lowfat = Tkinter.Button(top, text ="Change to low fat",command= lambda: info("low-fat"),width=40, height=2, wraplength=40)
Lowcarb = Tkinter.Button(top, text ="Change to low carb",command= lambda: info("low-carb") ,width=40, height=2, wraplength=40)
Bake = Tkinter.Button(top, text ="Change from bake to stir fry",command= lambda: info("baketostir") ,width=40, height=2, wraplength=40)
Normal = Tkinter.Button(top, text ="Submit Recipe Url",command= lambda: info("normal"),width=40, height=2, wraplength=40)


w = Text(top, width=40, height=1,pady=0)
w2 = Text(top, width=40, height=1,pady=0)


w.insert(INSERT, "Enter the URL to get the recipe.")
w2.insert(INSERT, "Click a button to transform it.")

w.grid(row=0, column=0)
w2.grid(row=1, column=0)
Vege.grid(row=2,column=0)
Vegan.grid(row=2,column=1)
Pesc.grid(row=2,column=2)
Lact.grid(row=3,column=0)
Lowfat.grid(row=3,column=1)
Lowcarb.grid(row=3,column=2)
Bake.grid(row=4,column=0)
Normal.grid(row=0,column=2)



top.mainloop()

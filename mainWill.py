#STATIC_DEPS=true sudo pip install lxml
#pip install requests
from lxml import html
import requests
import json
from collections import OrderedDict
from parseRecipe import parseRecipe
from transformation import toLactoseFree


# link = raw_input('Copy an allrecipes link here\n')
# parseRecipe(link)

print "1. Lactose-free"
print "2. insert"
choice = raw_input('Select a transformation by number\n')
toLactoseFree()
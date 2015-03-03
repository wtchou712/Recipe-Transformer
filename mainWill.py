#STATIC_DEPS=true sudo pip install lxml
#pip install requests
from lxml import html
import requests
import json
from collections import OrderedDict
from parseRecipe import parseRecipe

link = raw_input('Copy an allrecipes link here\n')
parseRecipe(link)

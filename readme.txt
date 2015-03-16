First, install the appropriate libraries for parsing html by running the code below in the terminal

STATIC_DEPS=true sudo pip install lxml
pip install requests

To run, the program, run: "python main.py". A GUI should pop up with a text input box on the top middle of the GUI for you to paste a recipe URL from allrecipes.com. 
Then click "Submit Recipe URL" to parse the recipe and view the recipe in the GUI below. On the left side of the GUI there are various buttons to transform the recipe.
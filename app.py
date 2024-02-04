from flask import Flask, request, render_template # Import the Flask, request, and render_template classes
import requests # Import the requests library

app = Flask(__name__)  # Create a Flask application instance

@app.route('/') # Define a route for the default URL, which loads the form
def home():
    return render_template('index.html') # Render the index.html template

@app.route('/search', methods=['POST']) # Define a route for the URL /search, which accepts POST requests
def search():
    ingredients = request.form.get('ingredients', '')
    diet = request.form.get('diet', '')  # Get the diet from the form
    intolerances = request.form.get('intolerances', '')  # Get the intolerances from the form

    api_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients, # Include the ingredients in the parameters
        'diet': diet,  # Include the diet in the parameters
        'intolerances': intolerances,  # Include the intolerances in the parameters
        'apiKey': '5cd3f3ead8a04b7e90e5bf5d7f9b7de5'  # This is the API key, which it makes the request to the API
    }

    response = requests.get(api_url, params=params) # Send a GET request to the API URL with the parameters
    data = response.json() # Convert the response from the API to a Python dictionary

    print(f'API response: {data}') # Print the response from the API to the terminal

    recipes = data   # Assign the data from the API to the recipes variable

    return render_template('results.html', recipes=recipes)  # Render the results.html template with the recipes

@app.route('/recipe/<int:recipe_id>')  # Define a route for URLs like /recipe/123
def recipe(recipe_id):  # Start a function that takes a recipe ID as an argument
    api_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'  # Define the API URL, inserting the recipe ID
    params = {'apiKey': '5cd3f3ead8a04b7e90e5bf5d7f9b7de5'}  # Define the parameters for the API request, including your API key

    response = requests.get(api_url, params=params)  # Send a GET request to the API URL with the parameters

    data = response.json()  # Convert the response from the API to a Python dictionary

    recipe = data  # Assign the data from the API to the recipe variable

    if recipe['instructions']:  # If the recipe has instructions
        recipe_steps = recipe['instructions'].split('.')  # Split the instructions into steps at each period
    else:  # If the recipe doesn't have instructions
        recipe_steps = []  # Define an empty list of steps

    return render_template('recipe.html', recipe=recipe, recipe_steps=recipe_steps)  # Render the recipe.html template with the recipe and steps

if __name__ == '__main__':
    app.run(debug=True)  # It runs the flask server in debug mode if usere entering by this point
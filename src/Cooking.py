import Methods

print("Right click on the first (top-right) cooking ingredient minus button")
print("for best results try to click as center in the button as possible")

print("THIS SCRIPT IS INEFFICIENT, RUN 'BetterCooking.py' FOR BETTER RESULTS")
x,y = Methods.getPosition()

ingredients = Methods.createIngredients(x,y) # creates a list of ingredients with the correct position of the buttons

print("Clearing previous values...")

Methods.ClearCooking(ingredients) # makes sure all ingredients are set to 0

print("Done clearing!")

print("start cooking...")
for ingredient in ingredients:
    print("setting ingredient")
    Methods.SetIngredient(ingredient,x,y) # sets all the ingredients

print("Done cooking!")



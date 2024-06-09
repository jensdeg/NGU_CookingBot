import Methods
from itertools import combinations

print("Right click on the first (top-right) cooking ingredient minus button")
print("for best results try to click as center in the button as possible")
x,y = Methods.getPosition()

ingredients = Methods.createIngredients(x,y) # creates a list of ingredients with the correct position of the buttons
print("Starting program, Press 'n' to stop")

print("Clearing previous values...")

Methods.ClearCooking(ingredients) # makes sure all ingredients are set to 0

print("Done clearing!")

nopeaks = []

# Adding peaks to the ingredient
print("Checking peaks")
for ingredient in ingredients:
    peaks = Methods.checkPeak(ingredient,x,y)
    ingredient.addpeaks(peaks[0])
    if len(peaks[0]) == 0: # for if there are no peaks
        nopeaks.append(ingredient)
    print("Found peak(s) at: {}".format(peaks[0]))
print("Done Checking peaks!")


# get pairs of ingredients that contain the same peaks
    
same_peak_ingredients = []

# Iterate through combinations of ingredients
for idx1, idx2 in combinations(range(len(ingredients)), 2):
    if Methods.compare_arrays(ingredients[idx1].Peaks, ingredients[idx2].Peaks):
        same_peak_ingredients.append([ingredients[idx1], ingredients[idx2]])

print("Start Cooking....")

for pair in same_peak_ingredients:
    print("Checking pair")
    Methods.setPair(pair,x,y)

for ingredient in nopeaks:
    Methods.SetIngredient(ingredient,x,y)


print("didn't get 100%, sorry!")
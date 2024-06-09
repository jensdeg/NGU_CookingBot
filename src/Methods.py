import win32api
import time
from ingredient import Ingredient
import pyautogui
import pytesseract
from scipy.signal import find_peaks
import keyboard


def CheckStopping():
    if keyboard.is_pressed('n'):
        print("Stopping Bot")
        exit()


def getPosition():
    # from https://stackoverflow.com/questions/165495/detecting-mouse-clicks-in-windows-using-pythonimport pyautogui
    state_right = win32api.GetKeyState(0x02)  # right button down = 0 or 1. Button up = -127 or -128

    
    while True:
        a = win32api.GetKeyState(0x02)

        if a != state_right:  # Button state changed
            state_right = a
            if a < 0:
                x,y = pyautogui.position()
                return x, y
        time.sleep(0.001)

def createIngredients(x,y):
    ingredients = []
    xDistance = 420
    yDistance = 135
    buttonDistance = 35

    for i in range(4):
        a = x
        b = y + (i*yDistance)
        ingredients.append(Ingredient([a,b-buttonDistance],[a,b]))

    # adding remaining 4 ingredients (right row)
    for i in range(4):
        a = x + xDistance
        b = y + (i*yDistance)
        ingredients.append(Ingredient([a,b-buttonDistance],[a,b]))
    
    return ingredients

def ClearCooking(ingredients):
    # clearing previous ingredient values
    for ingredient in ingredients:
        for i in range(20):
            CheckStopping()
            pyautogui.click(ingredient.minusPos)

def GetCookingEfficiency(x,y):

    CheckStopping()

    screenshotx = x + 190
    screenshoty = y + 490
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    img = pyautogui.screenshot(region=(screenshotx, screenshoty, 120, 35))

    text = pytesseract.image_to_string(img)

    text = text.replace("%","").replace("+","").replace(",",".").replace("\n","")

    try:
        number = float(text)
    except:
        number = 0
        print("got an invalid number, might effect outcome")
    if number == 100:
            print("Got 100%, Done cooking!!")
            exit()
    return number

def SetIngredient(ingredient,x,y):
    mealEfficiency = []

    for i in range(20):
        if i == 0:
            mealEfficiency.append(GetCookingEfficiency(x,y))
        pyautogui.click(ingredient.plusPos)
        mealEfficiency.append(GetCookingEfficiency(x,y))

    max_value = max(mealEfficiency)
    index = mealEfficiency.index(max_value)

    for i in range(20-index):
        CheckStopping()
        pyautogui.click(ingredient.minusPos)

    # for index, number in enumerate(mealEfficiency):
    #     print("{}: {}".format(index,number))
    
    return mealEfficiency

def checkPeak(ingredient, x,y):
    mealEfficiency = []

    for i in range(20):
        if i == 0:
            mealEfficiency.append(GetCookingEfficiency(x,y))
        pyautogui.click(ingredient.plusPos)
        mealEfficiency.append(GetCookingEfficiency(x,y))

    max_value = max(mealEfficiency)

    for i in range(20):
        CheckStopping()
        pyautogui.click(ingredient.minusPos)
    
    average_distance = getAverageDistance(mealEfficiency)
    
    peaks = find_peaks(mealEfficiency, threshold=average_distance)

    return peaks

def getAverageDistance(mealefficiency):
    mean = sum(mealefficiency) / len(mealefficiency)

    # Step 2: Calculate distances of each number from the mean
    distances = [abs(num - mean) for num in mealefficiency]

    # Step 3: Calculate the average distance
    average_distance = sum(distances) / len(distances)

    # print("Average distance from the mean:", average_distance)
    return average_distance

def compare_arrays(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if isinstance(arr1[i], list) and isinstance(arr2[i], list):
            if not compare_arrays(arr1[i], arr2[i]):
                return False
        elif arr1[i] != arr2[i]:
            return False
    return True

def setPair(pair, x,y):
    best_peak = 0
    best_pair_amount = 0
    best_max_value = 0

    for peak in pair[0].Peaks:
        PeakEfficiency = []
        for i in range(peak):
            CheckStopping()
            pyautogui.click(pair[0].plusPos) 
        
        for i in range(20):
            if i == 0:
                PeakEfficiency.append(GetCookingEfficiency(x,y))
            pyautogui.click(pair[1].plusPos)
            PeakEfficiency.append(GetCookingEfficiency(x,y))
        
        max_value = max(PeakEfficiency)
        if best_max_value == 0:
            best_max_value = max_value
            best_peak = peak
            best_pair_amount = PeakEfficiency.index(max_value)
        elif best_max_value != 0:
            if max_value >= best_max_value:
                best_max_value = max_value
                best_peak = peak
                best_pair_amount = PeakEfficiency.index(max_value)
        
        for i in range(20):
            CheckStopping()
            pyautogui.click(pair[1].minusPos)
        for i in range(peak):
            CheckStopping()
            pyautogui.click(pair[0].minusPos)

    for i in range(best_peak):
        CheckStopping()
        pyautogui.click(pair[0].plusPos)
    for i in range(best_pair_amount):
        CheckStopping()
        pyautogui.click(pair[1].plusPos)
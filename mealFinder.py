import requests
from bs4 import BeautifulSoup


class MealFinder:
    URL = 'https://andrews-university.cafebonappetit.com/cafe/terrace-cafe/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    '''@mealname is a string for the name of the meal'''

    @staticmethod
    def getmeal(mealname, numEntries):
        meal = MealFinder.soup.find(id=mealname)

        meal_items = meal.find_all(class_="h4 site-panel__daypart-item-title")

        menuString = "Today's " + mealname + " options are: \n"

        for meal_item in meal_items[:numEntries]:
            menuString += meal_item.text.strip() + "\n"

        print(menuString)

        return menuString
 #TODO: Clean out "Upon request"
 #TODO: indicate that multiples are vegan
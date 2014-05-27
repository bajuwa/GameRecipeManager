##KINGDOM HEARTS - BIRTH BY SLEEP
##RECIPE MANAGER
##
##Created by: Kaylyn Garnett
##Date Created: Aug 5/12
##
##gameplan:
##    single list of items
##      - each item is stored as a list with itself being the first element,
##          followed by recipes for making it
##      - recipes must be formatted alphabetically
##    file manipulation to store updated info
##    basic ui to search/list/edit information

def generateAllCombos(items):
    combos = []
    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            combos.append([items[i], items[j]])
    return combos

def generateUsedRecipes(recipes):
    usedRecipes = []
    for i in range(0, len(recipes)):
        temp = recipes[i]
        for j in range(0, len(temp)):
            usedRecipes.append(temp[j])
    return usedRecipes

def addRecipe(recipe, ing1, ing2, items, allRecipes):
    if recipe in items:
        if [ing1, ing2] not in allRecipes[items.index(recipe)] and [ing2, ing1] not in allRecipes[items.index(recipe)]:
            if ["", ""] in allRecipes[items.index(recipe)]:
                allRecipes[items.index(recipe)] = [[ing1, ing2]] #make sure its double []!
            else:
                allRecipes[items.index(recipe)].append([ing1, ing2])
    else:
        items.append(recipe)
        allRecipes.append([[ing1, ing2]]) #make sure its double []!
    if ing1 not in items:
        itemList.append(ing1)
        recipeList.append(" ")
    if ing2 not in items:
        items.append(ing2)
        allRecipes.append(" ")

def printRecipe(recipe, item):
    print(item + ":", end = " ")
    for j in range(0, len(recipe)): #looks at multiple combos
        anotherTemp = recipe[j]
        for k in range(0, len(anotherTemp)): #looks at elements of combos
            print(anotherTemp[k], end = " ")
            if k != len(anotherTemp)-1:
                print("x", end = " ")
        if j != len(recipe)-1:
            print(",", end = " ")
        else:
            print("", end = "\n")
    

# the lists for overall items and recipes to be read from the file
#   THEY MUST BE ORDERED PROPERLY (indeces must correspond)
itemList = []
recipeList = []

fileContent = ""

# opens and reads the file to get the current info
try:
    itemFile = open("items.txt")
    try:
        fileContent = itemFile.read()
    finally:
        itemFile.close()
except IOError:
    pass

#takes the file information and divies it up into the appropriate lists
#splits it into a list, seperated by the new lines
fileContent = fileContent.split("\n")
if fileContent[0] == "":
    fileContent[0] = 0
    
for i in range(1, int(fileContent[0])+1):
    itemList.append(fileContent[i])
for j in range(int(fileContent[0])+1, int(fileContent[0])*2+1):
    recipeList.append(fileContent[j])
#edit the recipelist so they register as individual items
#first split apart multiple combos for same recipe
for k in range(0, len(recipeList)):
    recipeList[k] = recipeList[k].split(";")
    #then split apart the combos into individual items
    for l in range(0, len(recipeList[k])):
        tempElements = recipeList[k]
        tempElements[l] = tempElements[l].split(" ")
    recipeList[k] = tempElements



userInput = ""
options = (
    "Save",    #0
    "View Untested",    #1
    "View Recipes",     #2
    "Find Recipe",      #3
    "Search by Combo",  #4
    "Add Recipe",       #5
    "Add Bulk Nulls",   #6
    "Important Info!!"  #7
    )

while userInput != "quit": # quit

    if userInput == "1":  # view potentials
        allCombos = generateAllCombos(itemList)
        recipes = generateUsedRecipes(recipeList)
        for i in range(0, len(allCombos)):
            test = allCombos[i]
            if [test[0], test[1]] not in recipes and [test[1], test[0]] not in recipes and "null" not in allCombos[i]:
                print(test[0],test[1]+";")
            
    elif userInput == "2":  #view recipes
        for i in range(1, len(recipeList)): # start at 1 to avoid null
            printRecipe(recipeList[i], itemList[i])
        print()

    elif userInput == "3": #find recipe
        userInput = input("Enter Recipe Name: ").lower()
        if userInput in itemList:
            printRecipe(recipeList[itemList.index(userInput)], userInput)
        else:
            print("Item not found")

    elif userInput == "4": #search by combo
        ing1 = input("Enter Ingredient 1: ").lower()
        ing2 = input("Enter Ingredient 2: ").lower()        
        for i in range(0, len(recipeList)):
            if [ing1, ing2] in recipeList[i]:
                print(itemList[i])
            elif [ing2, ing1] in recipeList[i]:
                print(itemList[i])
        
        
    elif userInput == "5":  #add recipe
        tempInput1 = input("Enter Ingredient 1: ").lower()
        tempInput2 = input("Enter Ingredient 2: ").lower()
        userInput = input("Enter Recipe Name: ").lower()
        addRecipe(userInput, tempInput1, tempInput2, itemList, recipeList)

    elif userInput == "6": #add bulk null combos
        nullCombos = []
        userInput = input("Enter Item Name or 0 to stop: ").lower()
        while userInput != "0":
            #make sure to add items that aren't already in the database
            if userInput not in itemList: 
                itemList.append(userInput)
                recipeList.append("")
            nullCombos.append(userInput) #running list of items
            userInput = input("Enter Item Name or 0 to stop: ").lower()
        nullCombos = generateAllCombos(nullCombos) #generate all the combos
        #add these combos under null recipe
        for i in range(0, len(nullCombos)):
            ingredients = nullCombos[i]
            addRecipe("null", ingredients[0], ingredients[1], itemList, recipeList)
        
    elif userInput == "7":
        print("Things to know:")
        print("- single items with multiple words (like 'sliding dash'), must use a '-' instead of ' '.")
        print("- this program is case-insensitive")
        print("- use bulk nulls to deal with multiple items that don't allow a combo/recipe")
        print("- in-game tip: buy at least one copy of all items in moogle shop, build max exp, then categorize them using bulk nulls")
        print("- to remove a combo from the 'untested' list, add the combo as a recipe named 'null'")
        print("- avoid using untested until you have built an extensive 'null' recipe set (suggest using bulk nulls)")
        print("- use 'search by combo' to see if a certain combo will result in a proper recipe")
        print("- items don't need to be in the itemList in order to be used in a recipe (the act of adding a recipe/bulk nulls with automatically add it to the item list)")

    
    try:
        itemFile = open("items.txt", 'w')
        try:
            #first element is size of each list (same number)
            itemFile.write(str(len(itemList)) + "\n")
            #write each element on its own line
            for i in range(0, len(itemList)):
                itemFile.write(itemList[i] + "\n")
            #write combos for a single recipe on a single line,
            #each element separated by a space
            for j in range(0, len(recipeList)):
                #fill with a space if no combo is provided
                if recipeList[j] == " ":
                    itemFile.write(" ")
                else:
                    #grab a (set of) combos from the recipe list
                    tempCombos = recipeList[j]
                    #write each individual item down, seperating combos by ;
                    for k in range(0, len(tempCombos)): #a combo
                        tempElements = tempCombos[k]
                        for l in range(0, len(tempElements)): #an element of combo
                            itemFile.write(tempElements[l])
                            if l != len(tempElements)-1:
                                itemFile.write(" ")
                        if k != len(tempCombos)-1:
                            itemFile.write(";")
                if j != len(recipeList)-1:
                    itemFile.write("\n")
        finally:
            itemFile.close()
    except IOError:
        pass    
            
    print("")
    print("What would you like to do?")
    for i in range(0, len(options)):
          print(str(i) + "." + options[i])
    userInput = input("").lower()


#save things before quitting
try:
    itemFile = open("items.txt", 'w')
    try:
        #first element is size of each list (same number)
        itemFile.write(str(len(itemList)) + "\n")
        #write each element on its own line
        for i in range(0, len(itemList)):
            itemFile.write(itemList[i] + "\n")
        #write combos for a single recipe on a single line,
        #each element separated by a space
        for j in range(0, len(recipeList)):
            #fill with a space if no combo is provided
            if recipeList[j] == " ":
                itemFile.write(" ")
            else:
                #grab a (set of) combos from the recipe list
                tempCombos = recipeList[j]
                #write each individual item down, seperating combos by ;
                for k in range(0, len(tempCombos)): #a combo
                    tempElements = tempCombos[k]
                    for l in range(0, len(tempElements)): #an element of combo
                        itemFile.write(tempElements[l])
                        if l != len(tempElements)-1:
                            itemFile.write(" ")
                    if k != len(tempCombos)-1:
                        itemFile.write(";")
            if j != len(recipeList)-1:
                itemFile.write("\n")
    finally:
        itemFile.close()
except IOError:
    pass







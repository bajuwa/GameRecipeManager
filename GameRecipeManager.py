##RECIPE MANAGER
##
##Created by: Kaylyn Garnett
##Date Created: Nov 30/12

#in order to delete files:
import os

#in order to format option listings
import asciilib

##Purpose:  Read a specified file and return a list of items and recipes from it
def loadFile(nameOfFile):
    # opens and reads the file to get the current info
    recipeContent = ""
    itemContent = ""
    try:
        recipeFile = open(nameOfFile+"RecipeList.txt")
        itemFile = open(nameOfFile+"ItemList.txt")
        filterFile = open(nameOfFile+"FilterList.txt")
        try:
            recipeContent = recipeFile.read().split("\n")
            itemContent = itemFile.read().split("\n")
            filterContent = filterFile.read().split("\n")
        finally:
            recipeFile.close()
            itemFile.close()
            filterFile.close()
            print("Successfully loaded files for "+nameOfFile)
    except IOError:
        print("Error reading from file, exiting loadFile")
        return 1
                          
    #return first the recipe list, then the item list
    return [recipeContent, itemContent, filterContent]


##Purpose: Takes all the items in a given list and pairs them together
##          to make a complete list of all possible N item recipes, where N is specified by user
def generateAllCombos(items, numOfIngredientsPerRecipe, excludeFilter, includeFilter):
    combos = []
    items.sort()
    nameOfItems = []

    for item in items:
        itemName = item.split(" = ")[0]
        if itemName not in excludeFilter:
            nameOfItems.append(itemName)
    
    if includeFilter == [] or includeFilter == [""]:
        includeFilter = nameOfItems
    
    if numOfIngredientsPerRecipe == 1 or numOfIngredientsPerRecipe == "1":
        combos = includeFilter
        
    elif numOfIngredientsPerRecipe == 2 or numOfIngredientsPerRecipe == "2":
        for i in range(0, len(nameOfItems)):
            for j in range(i+1, len(nameOfItems)):
                if nameOfItems[i] in includeFilter or nameOfItems[j] in includeFilter:
                    combos.append(nameOfItems[i]+" + "+nameOfItems[j])

    elif numOfIngredientsPerRecipe == 3 or numOfIngredientsPerRecipe == "3":
        for i in range(0, len(nameOfItems)):
            for j in range(i+1, len(nameOfItems)):
                for k in range(j+1, len(nameOfItems)):
                    if nameOfItems[i] in includeFilter or nameOfItems[j] in includeFilter or nameOfItems[j] in includeFilter:
                        combos.append(nameOfItems[i]+" + "+nameOfItems[j]+" + "+nameOfItems[k])

    ##print("TEST: combos: "+str(combos))
    return combos

def generateAllUntestedCombos(items, recipes, numOfIngredients, excludeFilter, includeFilter):
        allRecipeIngredients = generateAllCombos(items, numOfIngredients, excludeFilter, includeFilter)
        allUntested = []

        #gather all the recipe ingredients that have been tested
        testedRecipeIngredients = []
        ##print("TEST: recipes: "+str(recipes))
        for recipe in recipes:
            ingredients = recipe.split(" = ")[1].split(" + ")
            ingredients.sort()
            testedRecipeIngredients.append(" + ".join(ingredients))
        ##print("TEST: testedRecipeIngredients: "+str(testedRecipeIngredients))
        
        #check each recipe to see if it has been tested or not
        for ingredients in allRecipeIngredients:
            if ingredients not in testedRecipeIngredients:
                allUntested.append(ingredients)

        return allUntested

##Purpose:  Adds another recipe to the current recipeList
def addRecipe(product, ingredients, itemList, recipeList):
    # format the recipe into appropriate form
    fullRecipe = product + " = "
    # make sure product and ing are all in itemlist
    addItemToList(product, "", itemList)
    for ing in ingredients:
        if fullRecipe[-3:] != " = ":
            fullRecipe += str(" + ")
        fullRecipe += ing
        addItemToList(ing, "", itemList)
    #make sure to remove trailing " + "
    #now add the newly formatted recipe to the recipeList
    if recipeList == [""]:
        recipeList[0] += fullRecipe[:-3]
    else:
        recipeList.append(fullRecipe[:-3])
    return 0

## Purpose: Use this method to add to item list to maintain list formatting
def addItemToList(itemToAdd, description, itemList):
    if type(itemToAdd) is str and len(itemToAdd) > 0:
        # each line of list accomodates a possible description, so nothing past " = " should be checked
        for item in itemList:
            if item.split(" = ")[0] == itemToAdd:
                return 1
        if itemList == [""]:
            itemList[0] = str(itemToAdd+" = "+description)
        else:
            itemList.append(itemToAdd+" = "+description)
        return 0
    else:
        return 1

def returnIndexOfItem(itemToFind, itemList):
    for i in range(0, len(itemList)):
        if itemToFind == itemList[i].split(" = ")[0]:
            return i
    return -1

##Purpose: Finds all recipes resulting in the given product and returns as list
def returnRecipesForProduct(product, recipeList):
    listOfRecipesForProduct = []
    for recipe in recipeList:
        if recipe.split(" = ")[0] == product:
            listOfRecipesForProduct.append(recipe)
    return listOfRecipesForProduct

##Purpose: Runs the confirmation process to accept either Y or N from the user
def confirmFromUser(confirmationMessage):
    userInput = input(confirmationMessage + " (Y/N) ").lower()
    while userInput not in ["y", "n"]:
        userInput = input(confirmationMessage + " (Y/N) ").lower()
    if userInput == "y":
        return True
    else:
        return False
        

# the lists for overall items and recipes to be read from the file
    
##RECIPE FILE INFO:  This file contains all the recipes that have been tried in a certain game
##every line is in the form:
##"name of product" = "name of ingerdient 1" + "optional ing2" + "..." + "last optional ing"

##ITEM FILE INFO:  This file contains all the items mentioned during this recipe management as well as an optional description
##every line is in the form:
##"name of item" = "optional description"

itemList = []
recipeList = []
untestedFilterList = []
currentGameManager = ""
gameFilesContent = []

#read the file that contains the names of all the gamefiles for user
try:
    gameFilesFile = open("GameFiles.txt", "r")
    try:
        gameFilesContent = gameFilesFile.read().split("\n")
    finally:
        gameFilesFile.close()
except IOError:
    print("Error: could not load gameFiles")
    input()
    quit()
        



fileManagementOptions = [
    ## File Management
    "N. New",
    "D. Delete",
    "L. Load", 
    "S. Save",
    "Q. Save and Quit"
    ]

recipeManagementOptions = [
    ## Recipe Management  
    "1. Add Recipe",
    "2. Delete Recipe",
    "3. Search by Product",      
    "4. Search by Ingredient", 
    "5. View All Recipes", 
    "6. View Untested",
    "7. Recipes From Inventory",
    "8. Untested From Inventory",
    "9. Set Untested-Filter",
    ]

itemManagementOptions = [
    ## Item Management
    "10. Add Item",
    "11. Delete Item",
    "12. Add Description",
    "13. Clear Description",
    "14. Search By Name",
    "15. Search By Description",
    "16. View All Items"
    ]

allOptions = [fileManagementOptions, recipeManagementOptions, itemManagementOptions]

#defualt user input
userInput = "l"

while userInput != "q": # quit

    if currentGameManager not in gameFilesContent: # if a game manager isn't already loaded, prompt to load
        userInput = "l"
        
    if gameFilesContent == [""]: # if there are no managers, prompt to create
        userInput = "n"


    # interpret user input
    if userInput == "n":
        # prompt user to create their first recipe manager
        userInput = input("Name of new game recipe list: ")
        try:
            # open up the file to create the file
            recipeListFile = open(userInput+"RecipeList.txt", "w+")
            itemListFile = open(userInput+"ItemList.txt", "w+")
            filterListFile = open(userInput+"FilterList.txt", "w+")
            gameFilesFile = open("GameFiles.txt", "a+")
            try:
                gameFilesFile.write("\n"+userInput)
                gameFilesFile.seek(0)
                gameFilesContent = gameFilesFile.read().split("\n")
                currentGameManager = userInput
            finally:
                recipeListFile.close()
                itemListFile.close()
                filterListFile.close()
                gameFilesFile.close()
        except:
            print("Could not create new recipe files")
            
        #load the file or else lists won't be updated
        lists = loadFile(userInput)
        if lists != 1:
            recipeList = lists[0]
            itemList = lists[1]
            untestedFilterList = lists[2]
            currentGameManager = userInput

    elif userInput == "d":
        # get user to choose which file manager to delete
        print("Which Game Recipe Manager would you like to delete?")
        for i in range(0, len(gameFilesContent)):
            print(str(i)+". "+gameFilesContent[i])
        userInput = input()

        # delete the manager at chosen index
        os.remove(gameFilesContent[int(userInput)]+"RecipeList.txt")
        os.remove(gameFilesContent[int(userInput)]+"ItemList.txt")
        os.remove(gameFilesContent[int(userInput)]+"FilterList.txt")

        gameFilesContent.remove(gameFilesContent[int(userInput)])

        #update GameFiles.txt
        try:
            gameFiles = open("GameFiles.txt", "w+")
            try:
                gameFiles.write("\n".join(gameFilesContent))
                gameFiles.seek(0)
                gameFilesContent = gameFiles.read().split("\n")
            finally:
                gameFiles.close()
        except:
            print("Error: could not update GameFiles.txt")
    
    elif userInput == "l": # load
        print("Which game would you like to load? ")
        for i in range(0, len(gameFilesContent)):
            print(str(i)+". "+gameFilesContent[i])
        userInput = input()
        if userInput.isdigit() and int(userInput) in range(0, len(gameFilesContent)):
            lists = loadFile(gameFilesContent[int(userInput)])
            if lists != 1:
                recipeList = lists[0]
                itemList = lists[1]
                untestedFilterList = lists[2]
                currentGameManager = gameFilesContent[int(userInput)]
        else:
            print("You've entered an invalid index number")

    elif userInput == "s": # save
        #save things before quitting
        try:
            recipeFile = open(currentGameManager+"RecipeList.txt", 'w')
            itemFile = open(currentGameManager+"ItemList.txt", 'w')
            filterFile = open(currentGameManager+"FilterList.txt", 'w')
            try:
                # write all recipes to file
                for i in range(0, len(recipeList)):
                    if i != len(recipeList)-1:
                        recipeFile.write(recipeList[i]+"\n")
                    else:
                        recipeFile.write(recipeList[i])

                # write all items to file    
                for j in range(0, len(itemList)):
                    if j != len(itemList)-1:
                        itemFile.write(itemList[j]+"\n")
                    else:
                        itemFile.write(itemList[j])

                # write all filters to file
                for k in range(0, len(untestedFilterList)):
                    if k != len(untestedFilterList)-1:
                        filterFile.write(untestedFilterList[k]+"\n")
                    else:
                        filterFile.write(untestedFilterList[k])
                        
            finally:
                recipeFile.close()
                itemFile.close()
                filterFile.close()
        except IOError:
            print("Error: changes may not have been saved")

        print(currentGameManager+" has been saved!")

    elif userInput == "1":  #add recipe
        # use a loop to grab any number of ingredients from user
        ingredients = []
        i = 1
        while userInput != "":
            userInput = input(str("Enter Ingredient "+str(i)+": ")).lower()
            i = i+1
            if userInput != "":
                ingredients.append(userInput)
        ingredients.sort()

        # check to see if a recipe using those exact ingredients has already been submitted
        ingredientsMatchRecipe = False
        recipeIndex = 0
        while ingredientsMatchRecipe == False and recipeIndex < len(recipeList):
            # set to True before comparisons, will turn to False is identical recipe is found
            ingredientsMatchRecipe = True

            # compare already known recipe ingredients with users chosen ingredients
            if len(recipeList[recipeIndex].split(" = ")) > 1:
                recipeIngredients = recipeList[recipeIndex].split(" = ")[1].split(" + ")
                for ingredient in ingredients:
                    if ingredient not in recipeIngredients:
                        ingredientsMatchRecipe = False
            else:
                ingredientsMatchRecipe = False
                    
            # increment the index to check next recipe
            recipeIndex += 1

        if ingredientsMatchRecipe:
            if confirmFromUser("The ingredients you listed already match an existing recipe, would you like to continue anyways?"):
                # instead of creating a new variable, just reuse this one if they wish to continue
                ingredientsMatchRecipe == False

        if ingredientsMatchRecipe == False:
            # grab the name of the product
            product = input("Enter Product Name: ").lower()

            # if the product is a new item, give option to add description
            productPresentBefore = False
            if returnIndexOfItem(product, itemList) < 0:
                productPresentBefore = True

            # create a confirmation message to show to the user to confirm the recipe
            confirmationMessage = 'Add "'+product+" = "
            for i in range(0, len(ingredients)):
                confirmationMessage += ingredients[i]
                if i < len(ingredients)-1:
                    confirmationMessage += " + "
            confirmationMessage += '" to your recipe list?'
            
            #only proceed if they said yes
            if confirmFromUser(confirmationMessage):
                addRecipe(product, ingredients, itemList, recipeList)

                # if the product is new, prompt user for some extra information
                #print("TEST: present:"+str(productPresentBefore)+" index:"+str(returnIndexOfItem(product, itemList)))
                if productPresentBefore and returnIndexOfItem(product, itemList) >= 0:
                    print(product+" is a new item!")
                    userInput = input("Enter an optional description: ")
                    itemList[itemList.index(product + " = ")] = product + " = " + userInput
                    if not confirmFromUser("Would you like to use this item when testing new recipes?"):
                        untestedFilterList.append(product)
                        print(product +"has been added to the filter list")
        
        
            

    elif userInput == "2": # delete recipe
        # print all recipes along with their indices
        for i in range(0, len(recipeList)):
            print(str(i)+". "+recipeList[i])
        userInput = input("Which recipe would you like to delete? ")

        #remove the selected recipe
        if userInput != "":
            print("The following recipe has been deleted: "+recipeList[int(userInput)])
            recipeList.remove(recipeList[int(userInput)])
                            
    elif userInput == "3": #search by product
        # get the name of the product the user wants a recipe for
        userInput = input("Enter Recipe Name: ").lower()
        for recipe in recipeList:
            if recipe.split(" = ")[0] == userInput:
                # print each recipe that matches the user's specified product
                print(recipe)

    elif userInput == "4": #search by ingredients
        # use a loop to grab any number of ingredients from user
        ingredients = []
        i = 1
        while userInput != "":
            userInput = input(str("Enter Ingredient "+str(i)+": ")).lower()
            if userInput != "":
                ingredients.append(userInput)
            i = i+1

        # iterate through recipe list to try to find matches
        recipesFound = []
        for recipe in recipeList:
            # grab a temporary list of ingredients for the current recipe
            tempListIngredients = recipe.split(" = ")[1].split(" + ")
            # make sure all user-specified ingredients are in the recipe
            isRecipeFound = True
            for ing in ingredients:
                # make sure of the order!  this checks that all user-specified ingredients are present
                ## print("TEST: "+ing+" not in "+str(tempListIngredients))
                if ing not in tempListIngredients:
                    isRecipeFound = False

            # print the recipe if it matches
            if isRecipeFound:
                print(recipe)
        
    elif userInput == "5":  #view recipes
        # simply print the entire recipe list as its already in user-readable format
        for recipe in recipeList:
            print(recipe)

    elif userInput == "6":  # view untested
        numOfIng = input("View Untested Recipes with 1, 2, or 3 ingredients? ")
        include = []
        while userInput != "":
            userInput = input("Must Include Ingredient: ")
            if userInput != "":
                include.append(userInput)
        untestedList = generateAllUntestedCombos(itemList, recipeList, numOfIng, untestedFilterList, include)
        for untested in untestedList:
            print(untested)

    elif userInput == "7": # recipes from inventory
        print("Enter items in your inventory to figure out what you could make.")
        
        # use a loop to grab any number of ingredients from user
        inventory = []
        while userInput != "":
            userInput = input(str("Enter Ingredient: ")).lower()
            inventory.append(userInput)

        # generate list of recipes user could use
        print("You can make one (or more) or the following recipes:")
        for recipe in recipeList:
            # grab the ingredients and set bool to default true
            ingredientsForRecipe = recipe.split(" = ")[1].split(" + ")
            canMakeRecipe = True
            # if one of the ingredients for the recipe is not listed in the user specified inventory, recipe cannot be made
            for ingredient in ingredientsForRecipe:
                if ingredient not in inventory:
                    canMakeRecipe = False
            # print recipe if it can be made
            if canMakeRecipe:
                print(recipe)

    elif userInput == "8": # untested from inventory
        print("Enter items in your inventory to figure out what you could test.")
        
        # use a loop to grab any number of ingredients from user
        inventory = []
        while userInput != "":
            userInput = input(str("Enter Ingredient: ")).lower()
            inventory.append(userInput)

        userInput = input("How many ingredients per recipe? ")
        untestedList = generateAllUntestedCombos(itemList, recipeList, userInput, untestedFilterList, inventory)

        # generate list of recipes user could use
        print("You can test one (or more) or the following untested recipes:")
        
        for recipe in untestedList:
            # grab the ingredients and set bool to default true
            ingredientsForRecipe = recipe.split(" + ")
            canMakeRecipe = True
            # if one of the ingredients for the recipe is not listed in the user specified inventory, recipe cannot be made
            for ingredient in ingredientsForRecipe:
                if ingredient not in inventory:
                    canMakeRecipe = False
            # print recipe if it can be made
            if canMakeRecipe:
                print(recipe)

    elif userInput == "9": # set up untested-filter
        while userInput != "3":
            print("Currently excluding these items from untested recipe list: ")
            for i in range(0, len(untestedFilterList)):
                print(str(i)+". "+untestedFilterList[i])
            userInput = input("1. Add\t\t2. Remove\t3. Back\n")
            if userInput == "1":
                while userInput != "":
                    userInput = input("Enter item to exclude: ")
                    if userInput != "":
                        untestedFilterList.append(userInput)
            elif userInput == "2":
                while userInput != "":
                    userInput = input("Remove item from filter at index number: ")
                    if userInput != "":
                        untestedFilterList.remove(untestedFilterList[int(userInput)])

    elif userInput == "10": # add item
        name = input("Name of item: ")
        desc = input("Optional description: ")
        addItemToList(name, desc, itemList)

    elif userInput == "11": # delete item
        # print all items along with their indices
        for i in range(0, len(itemList)):
            print(str(i)+". "+itemList[i])
        userInput = input("Which item would you like to delete? ")

        #remove the selected item
        if userInput != "":
            print("The following item has been deleted: "+itemList[int(userInput)])
            itemList.remove(itemList[int(userInput)])

    elif userInput == "12": # add description
        userInput = input("Which item would you like to add a description to? ")
        for item in itemList:
            itemName = item.split(" = ")[0]
            if itemName == userInput:
                print("Current Description: "+item.split(" = ")[1])
                userInput = input("New Description: ")
                itemList[itemList.index(item)] = itemName + " = " + userInput

    elif userInput == "13": # clear description
        # print all items along with their indices
        for i in range(0, len(itemList)):
            print(str(i)+". "+itemList[i])
        userInput = input("Which description would you like to clear? ")

        #remove the selected description
        if userInput != "":
            print("The following description has been cleared: "+itemList[int(userInput)])
            itemList[int(userInput)] = itemList[int(userInput)].split(" = ")[0] + " = "       

    elif userInput == "14": # search by item name
        userInput = input("Search for item by name: ")
        for item in itemList:
            if userInput in item.split(" = ")[0]:
                print(item)
                
    elif userInput == "15": # search by item description
        userInput = input("Search for item by description: ")
        wordsToSearchBy = userInput.lower().split(" ")
        for item in itemList:
            found = True
            for word in wordsToSearchBy:
                if word not in item.split(" = ")[1].lower():
                    found = False
            if found:
                print(item)
        
    elif userInput == "16":  # view all items
        for item in itemList:
            print(item)


    #make sure to sort lists in case changes were made
    itemList.sort()
    recipeList.sort()

    #pause to give user item to view output
    print()
    input("Press Enter to proceed")
    print()

    #only procede to user interaction if they have loaded a valid game manager
    if currentGameManager in gameFilesContent:
        # Display the users options, then get input 
        print("What would you like to do with "+currentGameManager+"?")
        print()
        # iterate through options and format and draw each of them
        for optionSet in allOptions:
            textFieldOptions = asciilib.TextField(optionSet)
            title = ""
            if optionSet == fileManagementOptions:
                title = "File Options:"
            elif optionSet == recipeManagementOptions:
                title = "Recipe Options:"
            elif optionSet == itemManagementOptions:
                title = "Item Options:"
            textFieldTitle = asciilib.TextField([title])
            formatted = asciilib.TextField.formatOptionsIntoRowsWithTitle(textFieldOptions, 2, 55, "left", textFieldTitle, "center")
            formatted.draw()
            print()
        userInput = input("").lower()

# user has chosen to quit, save files before stopping program
#save things before quitting
try:
    recipeFile = open(currentGameManager+"RecipeList.txt", 'w')
    itemFile = open(currentGameManager+"ItemList.txt", 'w')
    filterFile = open(currentGameManager+"FilterList.txt", 'w')
    try:
        # write all recipes to file
        for i in range(0, len(recipeList)):
            if i != len(recipeList)-1:
                recipeFile.write(recipeList[i]+"\n")
            else:
                recipeFile.write(recipeList[i])

        # write all items to file    
        for j in range(0, len(itemList)):
            if j != len(itemList)-1:
                itemFile.write(itemList[j]+"\n")
            else:
                itemFile.write(itemList[j])

        # write all filters to file
        for k in range(0, len(untestedFilterList)):
            if k != len(untestedFilterList)-1:
                filterFile.write(untestedFilterList[k]+"\n")
            else:
                filterFile.write(untestedFilterList[k])
                
    finally:
        recipeFile.close()
        itemFile.close()
        filterFile.close()
except IOError:
    print("Error: changes may not have been saved")

print(currentGameManager+" has been saved!")


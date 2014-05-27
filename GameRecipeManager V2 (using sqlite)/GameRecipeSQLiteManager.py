##RECIPE MANAGER
##
##Created by: Kaylyn Garnett
##Date Created: Nov 30/12
##Modified with SQLite: Feb 7/13


import os
import sqlite3
import asciilib

# functions
def getDatabaseNames(path):
    """ Looks in the directory 'path' and returns the list of
        names of database WITHOUT the .db file extension """
    # get the names of everything in the directory
    try:
        names = os.listdir(path)
    except:
        return 1
    
    databases = []

    # iterate through each item to check if it's a database
    for name in names:
        if name[-3:] == ".db" and os.path.isfile(path+"/"+name):
            #make sure it has the .db extension
            #make sure it's a file!  (folders could use fake extensions)
            databases.append(name[:-3])
            
    return databases

def selectDatabase(dbName):
    """ Loads a database by it's file name (without extension) and sets all appropriate variables """
    # make sure to grab the global variables instead of declaring local ones
    global listOfDatabases
    global connecteddb
    global cursor
    global currentDBName # don't forget to set this!
    try:  
        connecteddb = sqlite3.connect("databases/"+dbName+".db")
        cursor = connecteddb.cursor()
        currentDBName = dbName
    except:
        return 1

def formatRecipeIngredientsQuery(ingredientsList, maxNumOfIngredients):
    """ Takes the list of ingredients one would like to query about,
        as well as the maximum number of ingredients allowed in the table,
        and returns the format for the column selection and the ingredient query. """
    # format the given ingredients list, as well as the format required for the recipe table query
    columnQuery = '"select product from recipes where '
    
    for i in range(0, maxNumOfIngredients):
        # add the ingredient or "none" if no more ingredients are mentioned
        # add the "in between" or "ending" syntax for the query format
        columnQuery += "ing"+str(i+1)+"="            
        if i < len(ingredients):
            columnQuery += "'"+str(ingredients[i])+"'"
        else:
            columnQuery += "'None'"
        if i < maxNumOfIngredients-1:
            columnQuery += " and "

    #return both the columns involved and the ingredients query format
    return columnQuery


def confirmFromUser(confirmationMessage):
    """ Runs the confirmation process to accept either Y or N from the user. """
    userInput = input(confirmationMessage + " (Y/N) ").lower()
    while userInput not in ["y", "n"]:
        userInput = input(confirmationMessage + " (Y/N) ").lower()
    if userInput == "y":
        return True
    else:
        return False

def formatIngredientColumns(numOfIngredients):
    """ takes the number of ingredients wanted, then formats to be used in certain sql queries """
    if type(numOfIngredients) is int:
        sqlquery = "("
        for i in range(0, numOfIngredients):
            sqlquery += "ing"+str(i)
            if i < numOfIngredients-1:
                sqlquery += ", "
            else:
                sqlquery += ")"
        return sqlquery


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

# current loaded game
listOfDatabases = getDatabaseNames("databases")
currentDBName = None
connecteddb = None
cursor = None

#defualt user input
userInput = "l"

while userInput != "q": # quit

    # ensure that a set of game files/db has been loaded
    if connecteddb is None \
       or currentDBName not in listOfDatabases: # if a game manager isn't already loaded, prompt to load
        userInput = "l"
##        print("TEST: redirecting to load")
        
    if listOfDatabases == []: # if there are no managers, prompt to create
        userInput = "n"
##        print("TEST: redirecting to new")



    # interpret user input
    if userInput == "n":
        # prompt user to create their first recipe manager
        userInput = input("Name of new game recipe list: ")

        # create and load the default db
        selectDatabase(userInput)
        

    elif userInput == "d":
        # get user to choose which database file to delete
        print("Which Game Recipe Manager would you like to delete?")
        for i in range(0, len(listOfDatabases)):
            print(str(i)+". "+listOfDatabases[i])
        userInput = input()

        # delete the database at chosen index
        if currentDBName == listOfDatabases[int(userInput)]:
            print("The database "+str(listOfDatabases[int(userInput)])+" is currently in use, please load another before deleting it.")
        else:
            confirmation = input("Are you sure you wish to delete "+listOfDatabases[int(userInput)]+"? (Y/N)")
            if confirmation.lower() == "y":
                os.remove("databases/"+listOfDatabases[int(userInput)]+".db")
                print(listOfDatabases[int(userInput)]+" has successfully been deleted.")
                listOfDatabases.remove(listOfDatabases[int(userInput)])
            else:
                print("Delete aborted, returning to menu...")
    
    elif userInput == "l": # load
        print("Which database would you like to load?")
        # list the available databases with an index for users to choose
        for i in range(0, len(listOfDatabases)):
            print(str(i)+". "+listOfDatabases[i])
        userInput = input()

        # make sure input is a valid choive
        if userInput.isdigit() and int(userInput) in range(0, len(listOfDatabases)):
            selectDatabase(listOfDatabases[int(userInput)])
        else:
            print("You've entered an invalid index number")

    elif userInput == "s": # save
        #save things before quitting
        connecteddb.commit()
        print(currentDBName+" has been saved!")     

    elif userInput == "1":  #add recipe
        print("Currently Broken")  
        # use a loop to grab any number of ingredients from user
        ingredients = []
        while userInput != "":
            userInput = input(str("Enter Ingredient "+str(len(ingredients)+1)+": ")).lower()
            if userInput != "":
                ingredients.append(userInput)
                # if it's a new item, add it to the item database
                cursor.execute("select name from items where name = ?", [userInput])
                if len(cursor.fetchall()) == 0:
                    cursor.execute("insert into items (name) values (?)", [userInput])
                
        # sort the ingredients alphabetically for organization
        ingredients.sort()

        # make sure there are sufficient number of ingredient columns in the recipe table
        cursor.execute("select * from recipes")
        numOfIngredientColumns = len(cursor.fetchone())-2  # -2 for "product" and "num of ingredients"

        #if there aren't enough columns, iteratively add them
        while numOfIngredientColumns < len(ingredients):
            cursor.execute(str("ALTER TABLE recipes ADD COLUMN 'ing"+str(numOfIngredientColumns+1)+"' 'text'")) 

            #recalculate number of columns
            cursor.execute("select * from recipes")
            numOfIngredientColumns = len(cursor.fetchone())-2
            

        # then format to sql query standards to see if a recipe using those exact ingredients has already been submitted
        sqlQuery = formatRecipeIngredientsQuery(ingredients, numOfIngredientColumns)
        if len(cursor.execute(sqlQuery)) > 0:
            print("this recipe already exists for product: "+cursor.fetchone())
        else:
            # if recipe doesn't already exist, 
            # grab the name of the product
            product = input("Enter Product Name: ").lower()

            # if the product is a new item, make sure to add to the item database first
            if len(cursor.execute("select name from items where name = ?", product)) == 0:
                print(product+" is a new item!")
                description = input("Enter an optional description: ")
                if not confirmFromUser("Would you like to include this item when testing for new recipes?"):
                    filtered = 1
                else:
                    filtered = 0
                cursor.execute("insert into items (name, description, filtered) values (?, ?, ?)", [product, description, filtered])

            # finally, add recipe to database
            sql = "insert into recipes (product, "+str(formatIngredientColumns(len(ingredients))[1:])+" values (?"+[", ?"]*len(ingredients)+")"
            cursor.execute(sql, [product]+ingredients)
            print("Recipe has been added!")

    elif userInput == "2": # delete recipe
        print("Currently Unavailable/Broken")  
        # print all recipes along with their indices for user to choose from
        # remove the selected recipe and print a confirmation
                            
    elif userInput == "3": #search by product
        print("Currently Unavailable/Broken")  
        # get the name of the product the user wants a recipe for
        # print each recipe that matches the user's specified product

    elif userInput == "4": #search by ingredients
        print("Currently Unavailable/Broken")  
        # use a loop to grab any number of ingredients from user
        ingredients = []
        i = 1
        while userInput != "":
            userInput = input(str("Enter Ingredient "+str(i)+" (or enter to quit): ")).lower()
            if userInput != "":
                ingredients.append(userInput)
            i = i+1

        # find and print all recipes that use those ingredients
        
    elif userInput == "5":  #view recipes
        print("Currently Unavailable/Broken")  
        # print the entire recipe list

    elif userInput == "6":  # view untested
        print("Currently Unavailable/Broken")  
        # have user choose how many ingredients to be included in the recipes
        numOfIng = input("View Untested Recipes with 1, 2, or 3 ingredients? ")

        # iterate through ingredient input until user presses enter
        include = []
        while userInput != "":
            userInput = input("Must Include Ingredient: ")
            if userInput != "":
                include.append(userInput)

        # print all recipes that could be made from this list, but not already listed in the db

    elif userInput == "7": # recipes from inventory
        print("Currently Unavailable/Broken")  
        # this will take a list of items and return all successful recipes possible from the given list
        print("Enter items in your inventory to figure out what you could make.  Press Enter when done.")
        
        # use a loop to grab any number of ingredients from user
        inventory = []
        while userInput != "":
            userInput = input(str("Enter Ingredient: ")).lower()
            inventory.append(userInput)

        # generate list of recipes user could use and print to screen
        print("You can make one (or more) or the following recipes:")

    elif userInput == "8": # untested from inventory
        print("Currently Unavailable/Broken")  
        # this will take a list of items and return all untested recipes from the given list
        print("Enter items in your inventory to figure out what you could test.  Press Enter when done.")
        
        # use a loop to grab any number of ingredients from user
        inventory = []
        while userInput != "":
            userInput = input(str("Enter Ingredient: ")).lower()
            inventory.append(userInput)

        # have user choose how many ingredients to be included in the recipes
        numOfIng = input("View Untested Recipes with 1, 2, or 3 ingredients? ")
        
        # generate list of recipes user could use
        print("You can test one (or more) or the following untested recipes:")
        

    elif userInput == "9": # set up untested-filter
        print("Currently Unavailable/Broken")  
        #displays all items user does not want to appear when generating untested lists
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
        print("Currently Unavailable/Broken")  
        name = input("Name of item: ")
        desc = input("Optional description: ")
        #add item to list

    elif userInput == "11": # delete item
        print("Currently Unavailable/Broken")  
        # print all items along with their indices for user to choose from
        # remove the selected item

    elif userInput == "12": # add description
        print("Currently Unavailable/Broken")  
        # ask user which item they would like to describe
        userInput = input("Which item would you like to add a description to? ")
        # show current description, confirm user wants to change it
        # update description with users input

    elif userInput == "13": # clear description
        print("Currently Unavailable/Broken")  
        # print all items along with their indices for user to choose from
        # confirm description then remove the clear it       

    elif userInput == "14": # search by item name
        print("Currently Unavailable/Broken")  
        # get name of item to find
        userInput = input("Search for item by name: ")
        # display all items that contain the string the user gave
                
    elif userInput == "15": # search by item description
        print("Currently Unavailable/Broken")  
        # find a list of words for user to search descriptions with
        userInput = input("Search for item by description: ")
        wordsToSearchBy = userInput.lower().split(" ")
        # print all items with their descriptions that follow users inputs
        
    elif userInput == "16":  # view all items
        print("Currently Unavailable/Broken")  
        # print all items
        

    #pause to give user item to view output
    print()
    input("Press Enter to proceed")
    print()

    #only procede to user interaction if they have loaded a valid game manager
    if currentDBName in listOfDatabases:
        # Display the users options, then get input 
        print("What would you like to do with "+currentDBName+"?")
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
# save things before quitting
connecteddb.commit()
print(currentDBName+" has been saved!")


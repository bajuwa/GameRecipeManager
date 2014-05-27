

def convertGRMItemList(gameName):
    #try to open the file to grab it's contents
    try:
        itemFile = open(gameName+"ItemList.txt")
        itemList = itemFile.read().split("\n")
        filterFile= open(gameName+"FilterList.txt")
        filterList = filterFile.read().split("\n")
    finally:
        itemFile.close()
        filterFile.close()

    # make sure the list imported properly
    if len(itemList) == 0:
        return 1
    else:
        for item in itemList:
            itemName, itemDesc = item.split(" = ")
            dbQueryFormat = "('"+itemName+"', '"+itemDesc+"', None, None, None,"

            # if the item is "filtered", then denote that with a 1, any other integer is considered not filtered
            if itemName in filterList:
                dbQueryFormat += " 1),"
            else:
                dbQueryFormat += " 0),"
                
            print(dbQueryFormat)

def convertGRMRecipeList(gameName, maxNumOfIngredients):
    #try to open and read the file, one recipe per line
    try:
        recipeFile = open(gameName+"RecipeList.txt")
        recipeList = recipeFile.read().split("\n")
    finally:
        recipeFile.close()

    # make sure the list imported properly
    if len(recipeList) != 0:
        for recipe in recipeList:
            #split up the previous files format into product and individual ingredients
            product, ingredients = recipe.split(" = ")
            ingredients = ingredients.split(" + ")
            
            #format it into the format required for sql queries
            dbQueryFormat = str("('"+product+"'")
            for ingredient in ingredients:
                dbQueryFormat += ", '"+ingredient+"'"
                
            #fill the remaining spots with None's
            for null in range(0, maxNumOfIngredients-len(ingredients)):
                dbQueryFormat += ", None"
            
            # calculate and add the numOfIngredients column value
            dbQueryFormat += ", "+str(len(ingredients))+"),"
            #finally, print 
            print(dbQueryFormat)
    else:
        return 1

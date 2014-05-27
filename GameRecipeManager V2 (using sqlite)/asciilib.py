### Version: 0.1 ###
##Changes in this version:
##    - Library turned into classes: Drawings, Borders, Frames, TextFields, Jigsaws
##    - Seperated from DS-specific library
##    - Merged redundant methods by adding more parameters
##    - New Feature: Frames (can be used for resizeable banners)
##    - More support for importing personal ASCII art (formatting, saving/exporting)
##    - Drawing.overlayDrawings now uses outer-whitespace detection from top-bottom and vice versa for more accurate overlays


#To Do:
# Come up with some examples for Frames
# Add more to text class (bullets, numbers, add indent to formatParagraph)
# Add class/drawings: AsciiFont (utilize seperate files for each font)


#Imports
import math
import copy
import string


#######################
###Classes - Drawing###
#######################

#Purpose: A class to store information about a "drawing" and provide proper methods to modify the drawing
#Note: A drawing is an array of strings, where each string is a row of the drawing

class Drawing:
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########
    
    _original = []
    _drawing = []
    

    ########################
    #Methods - Init/Set/Get#
    ########################
    
    def __init__(self, arrayOfStrings):
        if type(arrayOfStrings) is not list:
            print("Error: parameter type mismatch in Drawing.__init__")
            print(type(arrayOfStrings))
            return 1
        for e in range(0, len(arrayOfStrings)):
            if type(arrayOfStrings[e]) is not str:
                print("Error: parameter type mismatch in arrayOfStrings in Drawing.__init__")
                return 1
        self._drawing = copy.deepcopy(arrayOfStrings)
        self._original = copy.deepcopy(arrayOfStrings)
        return

    def getDrawing(self):
        return self._drawing

    def getRow(self, rowIndex):
        if type(rowIndex) is not int or \
           rowIndex >= len(self._drawing) or \
           rowIndex < -1*(len(self._drawing)):
            print("Error: parameter type mismatch in Drawing.getRow")
            return 1
        return self._drawing[rowIndex]

    def getOriginal(self):
        return self._original

    def setDrawing(self, newDrawing):
        if type(newDrawing) is not list:
            print("Error: parameter type mismatch in Drawing.setDrawing")
            return 1
        for e in range(0, len(newDrawing)):
            if type(newDrawing[e]) is not str:
                print("Error: parameter type mismatch in Drawing.setDrawing")
                return 1
        self._drawing = copy.deepcopy(newDrawing)
        return

    def resetDrawing(self):
        self.setDrawing(copy.deepcopy(self._original))
        return

    def setOriginal(self, newOriginal):
        if type(newOriginal) is not list:
            print("Error: parameter type mismatch in Drawing.setOriginal")
            return 1
        for e in range(0, len(newOriginal)):
            if type(newOriginal[e]) is not str:
                print("Error: parameter type mismatch in Drawing.setOriginal")
                return 1
        self._original = copy.deepcopy(newOriginal)
        return 0

    def setRow(self, rowIndex, string):
        if type(rowIndex) is not int or \
           type(string) is not str:
            print("Error: parameter type mismatch in Drawing.setRow")
            return 1
        self._drawing[rowIndex] = string


    ############################
    #Methods - Abstract Getters#
    ############################
    ## Getters that calculate information based on the drawing ##
        
    #Purpose: Draws the drawing to the screen as an image, not as an array
    def draw(self):
        for i in range(0, len(self.getDrawing())):
            print(self.getRow(i))
        return
    
    #Purpose: Retrieves height by calculating the number of rows, aka the number of string elements in the array    
    def getHeight(self):
        return len(self.getDrawing())

    #Purpose: Retrieves the maximum width out of all the rows
    #Note: deals with the maximum to account for a non-buffered image with irregular width
    def getWidth(self):
        widthList = []
        for i in range(0, self.getHeight()):
            widthList.append(len(self.getDrawing()[i]))
        return max(widthList)
    
    #Purpose: returns a 2-element array specifying how many times the drawing can fit in a row of targetWidth and a column of targetHeight
    #Note: array is read: [how many can fit in a row of targetWidth, how many can fit in a column of targetHeight]
    def howManyCanFit(self, targetWidth, targetHeight):
        if type(targetWidth) is not int or \
           type(targetHeight) is not int:
            print("Error: parameter type mismatch in Drawing.howManyCanFit")
            return 1
        totalInRow = math.floor(targetWidth/len(self.getDrawing()[0]))
        totalInColumn = math.floor(targetHeight/len(self.getDrawing()))
        return [totalInRow, totalInColumn]

    #Purpose: Returns the number of instances of a certain char are found in a row, starting from the right
    def numOfCharsInRowFromRight(self, rowIndex, char):
        if type(rowIndex) is not int or \
           type(char) is not str or \
           len(char) != 1:
            print("Error: parameter type mismatch in Drawing.numOfCharsInRowFromRight")
            return 1
        count = 0
        tempRow = self.getRow(rowIndex)
        for i in range(len(self.getRow(rowIndex))-1, -1, -1): #iterate through chars in row, right to left
            if tempRow[i] == char:
                count += 1
            else:
                return count
        return count

    #Purpose: Returns the number of instances of a certain char are found in a row, starting from the right
    def numOfCharsInRowFromLeft(self, rowIndex, char):
        if type(rowIndex) is not int or \
           type(char) is not str or \
           len(char) != 1:
            print("Error: parameter type mismatch in Drawing.numOfCharsInRowFromLeft")
            return 1
        count = 0
        tempRow = self.getRow(rowIndex)
        for i in range(0, len(tempRow)): #iterate through chars in row, left to right
            if tempRow[i] == char:
                count += 1
            else:
                return count
        return count

    #Purpose: Returns the number of instances of a certain char are found in a column, starting from the bottom
    def numOfCharsInColumnFromTop(self, columnIndex, char):
        if type(columnIndex) is not int or \
           type(char) is not str or \
           len(char) != 1:
            print("Error: parameter type mismatch in Drawing.numOfCharsInColumnFromTop")
            return 1
        count = 0
        for i in range(0, len(self.getDrawing())): #iterate through rows, top to bottom
            tempRow = self.getDrawing()[i]
            if tempRow[columnIndex] == char:
                count += 1
            else:
                return count
        return count

    #Purpose: Returns the number of instances of a certain char are found in a column, starting from the bottom
    def numOfCharsInColumnFromBottom(self, columnIndex, char):
        if type(columnIndex) is not int or \
           type(char) is not str or \
           len(char) != 1:
            print("Error: parameter type mismatch in Drawing.numOfCharsInColumnFromBottom")
            return 1
        count = 0
        for i in range(len(self.getDrawing())-1, -1, -1): #iterate through rows, bottom to top, if char is right
            tempRow = self.getDrawing()[i]
            if tempRow[columnIndex] == char:
                count += 1
            else:
                return count
        return count

    #Purpose: Returns boolean value based on whether the row is empty/whitespace or not
    def isRowEmpty(self, rowIndex):
        if type(rowIndex) is not int:
            print("Error: parameter type mismatch in Drawing.numOfCharInDrawing")
            return 1
        #If, by scanning through the row, it hits the end of the row before a non-whitespace character, it's an empty row
        tempRow = self.getRow(rowIndex)
        for i in range(0, len(tempRow)):
            if tempRow[i] != " ":
                return False
        return True

    #Purpose: Returns the number of times an instance of parameter char occurs in a row of a drawing
    def numOfCharInRow(self, rowIndex, char):
        if type(rowIndex) is not int or \
           rowIndex not in range(0, len(self.getDrawing())) or \
           type(char) is not str or \
           len(char)!= 1:
            print("Error: parameter type mismatch in Drawing.numOfCharInRow")
            return 1
        
        count = 0
        for character in self.getRow(rowIndex):
            if character == char:
                count += 1
        return count
        
    #Purpose: Returns the number of times an instance of parameter char occurs in a drawing
    def numOfCharInDrawing(self, char):
        if type(char) is not str or \
           len(char)!= 1:
            print("Error: parameter type mismatch in Drawing.numOfCharInDrawing")
            return 1
        count = 0
        for i in range(0, len(self.getDrawing())):
            count += self.numOfCharInRow(i, char)
            
        return count
    
    ##############################
    #Methods - Setters: Buffering#
    ##############################
    #Warning: These methods directly modify _drawing!

    #Purpose: Trims excess whitespace from edges so drawing is resized to smallest possible dimensions
    #Notes: As an example, it will take a buffered image and get rid of the whitespace that might have been added
    def trim(self):
        #make sure image is buffered to avoid errors
        self.bufferAlign("center", "center", self.getWidth(), self.getHeight())
        
        #trim tops and bottoms of empty rows
        while self.isRowEmpty(0) == True:
            self.setDrawing(self.getDrawing()[1:])
        while self.isRowEmpty(-1) == True:
            self.setDrawing(self.getDrawing()[:-1])

        #then trim sides
        emptyRightSpace = []
        emptyLeftSpace = []
        for i in range(0, self.getHeight()):
            emptyRightSpace.append(self.numOfCharsInRowFromRight(i, " "))
            emptyLeftSpace.append(self.numOfCharsInRowFromLeft(i, " "))
        self.bufferAlign("left", "center", self.getWidth()-min(emptyRightSpace), self.getHeight())
        self.bufferAlign("right", "center", self.getWidth()-min(emptyLeftSpace), self.getHeight())

        return 0


    #Purpose: adds/removes rows/characters to fit a certain dimension and alignment
    #Note: RLalign refers to "left", "center", or "right"; TBalign refers to "top", "center", or "bottom"
    def bufferAlign(self, LRAlign, TBAlign, targetWidth, targetHeight):
        if LRAlign not in ["center", "left", "right"] or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(targetWidth) is not int or \
           type(targetHeight) is not int:
            print("Error: parameter type mismatch in Drawing.bufferAlign")
            return 1
        #Make height changes
        differenceInHeights = targetHeight - len(self.getDrawing())
        topBuffer = math.ceil(differenceInHeights/2)
        bottomBuffer = math.floor(differenceInHeights/2)
        if TBAlign == "top":
            if differenceInHeights >= 0:
                self._drawing += [" "*self.getWidth()] * differenceInHeights
            else:
                self._drawing = self._drawing[:targetHeight]
        elif TBAlign == "center":
            if differenceInHeights >= 0:
                self._drawing = [" "] * topBuffer + self._drawing + [" "] * bottomBuffer
            else:
                self._drawing = self._drawing[-1*topBuffer:bottomBuffer]
        elif TBAlign == "bottom":
            if differenceInHeights >= 0:
                self._drawing = [" "*self.getWidth()] * differenceInHeights + self._drawing
            else:
                self._drawing = self._drawing[-targetHeight:]
        else:
            return 1 #signifies an error

        
        #Make width changes
        for i in range(0, len(self._drawing)):
            #calculate adjustments - if difference is odd, an extra space will be added to the right/top
            differenceInWidth = targetWidth - len(self.getRow(i))
            rightBuffer = math.ceil(differenceInWidth/2)
            leftBuffer = math.floor(differenceInWidth/2)
            tempRow = self._drawing[i]
            if LRAlign == "left":
                if differenceInWidth >= 0:
                    self._drawing[i] += " " * differenceInWidth
                else:
                    self._drawing[i] = tempRow[:targetWidth]   
            elif LRAlign == "center":
                if differenceInWidth >= 0:
                    self._drawing[i] = " "*leftBuffer + tempRow + " "*rightBuffer
                else:
                    self._drawing[i] = tempRow[-1*leftBuffer:rightBuffer]
            elif LRAlign == "right":
                if differenceInWidth >= 0:
                    self._drawing[i] = " " * differenceInWidth + self._drawing[i]
                else:
                    self._drawing[i] = tempRow[-targetWidth:]
            else:
                return 1 #signifies an error
                
        return 0
    #END BUFFERALIGN
    
    #Purpose: Adds a simple, 1-char width border around the edge of a drawing
    #Note: To remove the border, simply trim it to 1 less width/height
    def addBorder(self, border, padding):
        #run through a check to make sure you're attaching a frame
        if type(border) is not Border or \
           type(padding) is not int:
            print("Error: parameter type mismatch in Drawing.addBorder")
            return 1

        #now set up and add the border around the edge of the drawing
        borderedDrawing = []
        height = self.getHeight()
        width = self.getWidth()
        arrayOfCorners = border.getCorners()
        arrayOfBorders = border.getBorders()
        # top of border
        borderedDrawing.append(arrayOfCorners[0] + arrayOfBorders[0] * (width+(padding*2)) + arrayOfCorners[1])
        borderedDrawing.extend([arrayOfBorders[3] + " "*(width+(padding*2)) + arrayOfBorders[1]]*padding)
        # attaches the contents of the display
        for i in range(0, height):
            sampleLine = self.getRow(i)
            # attaches the appropriate line of the objects from top to bottom
            borderedDrawing.append(arrayOfBorders[3] + " "*padding + sampleLine + " "*padding + arrayOfBorders[1])

        # attaches bottom of the border
        borderedDrawing.extend([arrayOfBorders[3] + " "*(width+(padding*2)) + arrayOfBorders[1]]*padding)
        borderedDrawing.append(arrayOfCorners[2] + arrayOfBorders[2] * (width+(padding*2)) + arrayOfCorners[3])
        self.setDrawing(borderedDrawing)
        return 0
    

    #########################
    #Methods - Class Methods#
    #########################
    #These classes are meant to be used to return new values/drawings, and should not be called by an object instance

    #Purpose: Return the max height of drawings given in an array of drawings
    def getMaxHeight(arrayOfDrawings):
        if type(arrayOfDrawings) is not list:
            print("Error: parameter type mismatch in Drawing.getMaxHeight")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.getMaxHeight")
                return 1
        heightsOfDrawings = []
        for i in range(0, len(arrayOfDrawings)):
            tempDrawing = arrayOfDrawings[i]
            heightsOfDrawings.append(tempDrawing.getHeight())
        return max(heightsOfDrawings)

    #Purpose: Return the max width of drawings given in an array of drawings
    def getMaxWidth(arrayOfDrawings):
        if type(arrayOfDrawings) is not list:
            print("Error: parameter type mismatch in Drawing.getMaxWidth")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.getMaxWidth")
                return 1
        widthsOfDrawings = []
        for i in range(0, len(arrayOfDrawings)):
            tempDrawing = arrayOfDrawings[i]
            widthsOfDrawings.append(tempDrawing.getWidth())
        return max(widthsOfDrawings)

    #Purpose: Returns a coordinate array corresponding to the n-th instance of char in the drawing
    def getCoordOfChar(self, char, nthInstance):
        if type(char) is not str or\
           len(char) != 1 or \
           type(nthInstance) is not int:
            print("Error: parameter type mismatch in Drawing.getCoordOfChar")
            return 1
        count = 0
        for i in range(0, self.getHeight()): #iterate over rows
            tempRow = self.getRow(i)
            for j in range(0, self.getWidth()):  #iterate over characters in a row
                tempChar = tempRow[j]
                if tempChar == char:
                    count += 1
                    if count == nthInstance:
                        return [j, i]
        #if nthInstance was not found:
        return 0
        
    #Purpose: Turns a drawing into a tiled image within specific requirements of how many in a row/column
    #Notes: Padding refers to how much whitespace is in between each tile image
    def createTiledDrawingFromTileNums(drawing, numInRow, numInColumn, padding):
        if type(drawing) is not Drawing or \
           type(numInRow) is not int or \
           type(numInColumn) is not int or \
           type(padding) is not int:
            print("Error: parameter type mismatch in Drawing.createTiledDrawingFromTileNums")
            return 1
        singleRow = []
        for i in range(0, numInRow): #must iterate a deepcopy in order to avoid passing by reference
            singleRow.append(copy.deepcopy(drawing))
        singleRow = Drawing.combineIntoRow(singleRow, "center", padding)
        tiledImage = []
        for j in range(0, numInColumn):
            tiledImage.append(copy.deepcopy(singleRow))
        tiledImage = Drawing.combineIntoColumn([singleRow] * numInColumn, "center", padding)
        return tiledImage

    #Purpose: Turns a drawing into a tiled image within specific WxH dimensions
    #Notes: This image will cut off any excess characters outside the given dimensions
    def createTiledDrawingFromDimensions(drawing, targetWidth, targetHeight, padding):
        if type(drawing) is not Drawing or \
           type(targetWidth) is not int or \
           type(targetHeight) is not int or \
           type(padding) is not int:
            print("Error: parameter type mismatch in Drawing.createTiledDrawingFromDimensions")
            return 1
        numInDimensions = drawing.howManyCanFit(targetWidth, targetHeight)
        tiledDrawing = Drawing.createTiledDrawingFromTileNums(drawing, numInDimensions[0]+1, numInDimensions[1]+1, padding)
        tiledDrawing.bufferAlign("center", "center", targetWidth, targetHeight)
        return tiledDrawing

    #Purpose: Takes 2 drawings, replaces the character on the first image with the characters from the second image, skipping any CHARs in the overlaying drawing
    #Note: Will only ignore the CHARs on the outside of the drawing, for example: if char = " ", then only whitespace outside the drawing will be ignored
    #Note: Although it will buffer each image to the same dimensions, its best to do that yourself before calling this function to make sure they align properly
    def overlayDrawings(baseDrawing, overlayDrawing, char, LRAlign, TBAlign):
        if type(baseDrawing) is not Drawing or \
           type(overlayDrawing) is not Drawing or \
           LRAlign not in ["center", "left", "right"] or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(char) is not str or \
           len(char) != 1:
            print("Error: parameter type mismatch in Drawing.overlayDrawings")
            return 1
        #make sure they are the same size
        copyDrawings = [copy.deepcopy(baseDrawing), copy.deepcopy(overlayDrawing)]
        copies = Drawing.bufferToSameHeight(copyDrawings, TBAlign, Drawing.getMaxHeight(copyDrawings))
        copies = Drawing.bufferToSameWidth(copies, LRAlign, Drawing.getMaxWidth(copies))
        baseCopy = copies[0]
        overlayCopy = copies[1]

        for i in range(0, len(baseCopy.getDrawing())): #iterate over rows
            for j in range(0, len(baseCopy.getRow(i))): #iterate over columns
                # use numOfChars to ensure that even intended spaces in the middle of a drawing get copied over
                if (j >= overlayCopy.numOfCharsInRowFromLeft(i, char)) and (j < (len(overlayCopy.getRow(i)) - overlayCopy.numOfCharsInRowFromRight(i, char))):
                    if (i >= overlayCopy.numOfCharsInColumnFromTop(j, char)) and (i < (overlayCopy.getHeight() - overlayCopy.numOfCharsInColumnFromBottom(j, char))):
                        baseCopy.setRow(i, baseCopy.getRow(i)[:j] + overlayCopy.getRow(i)[j] + baseCopy.getRow(i)[j+1:])
        return baseCopy

    #Purpose: Buffers each drawing of an array of drawings to the same height
    def bufferToSameHeight(arrayOfDrawings, TBAlign, targetHeight):
        if type(arrayOfDrawings) is not list or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(targetHeight) is not int:
            print("Error: parameter type mismatch in Drawing.bufferToSameHeight")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.bufferToSameHeight")
                return 1
        copyDrawings = []
        for i in range(0, len(arrayOfDrawings)):
            copyDrawings.append(copy.deepcopy(arrayOfDrawings[i]))
        for j in range(0, len(copyDrawings)):
            tempDrawing = copyDrawings[j]
            tempDrawing.bufferAlign("center", TBAlign, tempDrawing.getWidth(), targetHeight)
            copyDrawings[j] = tempDrawing
        return copyDrawings
    
    #Purpose: Combine an array of drawings, in order, in a row, aligned as specified
    #Notes: combines them edge-to-edge, with a certain amount of padding between each image
    def combineIntoRow(arrayOfDrawings, TBAlign, padding):
        if type(arrayOfDrawings) is not list or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(padding) is not int:
            print("Error: parameter type mismatch in Drawing.combineIntoRow")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.combineIntoRow")
                return 1
        copyDrawings = []
        for i in range(0, len(arrayOfDrawings)):
            copyDrawings.append(copy.deepcopy(arrayOfDrawings[i]))
        copyDrawings = Drawing.bufferToSameHeight(copyDrawings, TBAlign, Drawing.getMaxHeight(arrayOfDrawings))
        rootPseudoDrawing = copyDrawings[0].getDrawing()  #takes the first image, and modifies it by extending the strings/rows with that of other drawings
        for k in range(0, len(rootPseudoDrawing)): #iterate over rows
            for l in range(1, len(copyDrawings)): #iterate over drawings
                #since we start at index 1, add befores before each image (this also prevents excess buffering at the end
                rootPseudoDrawing[k] += " " * padding
                samplePseudoDrawing = copyDrawings[l].getDrawing()
                rootPseudoDrawing[k] += samplePseudoDrawing[k]
        completeRowDrawing = Drawing(rootPseudoDrawing)
        return completeRowDrawing

    #Purpose: Buffers each drawing to be combined into a row of a specific width
    def combineIntoRowWidth(arrayOfDrawings, LRAlign, TBAlign, targetWidth):
        if type(arrayOfDrawings) is not list or \
           LRAlign not in ["center", "left", "right"] or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(targetHeight) is not int:
            print("Error: parameter type mismatch in Drawing.combineIntoRowWidth")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.combineIntoRowWidth")
                return 1
        bufferedRow = copy.deepcopy(arrayOfDrawings) #make sure to copy to you're not modifying the original
        #calculate total width of combined drawings
        totalWidth = 0
        for i in range(0, len(bufferedRow)):
            totalWidth += bufferedRow[i].getWidth()
        differenceInWidth = targetWidth - totalWidth
        #calculate how much each drawing gets buffered
        individualBufferPadding = math.floor(differenceInWidth/len(bufferedRow))
        #buffer each image
        for j in range(0, len(bufferedRow)):
            bufferedRow[j].bufferAlign(LRAlign, TBAlign, bufferedRow[j].getWidth() + individualBufferPadding, bufferedRow[j].getHeight())
        #Note: padding = 0 because focus is on equally spaced images, not padding in between them
        #since individualBufferPadding was rounded down, make sure to return the image after it's been buffered to the correct width
        bufferedRow = Drawing.combineIntoRow(bufferedRow, TBAlign, 0)
        bufferedRow.bufferAlign(LRAlign, TBAlign, targetWidth, bufferedRow.getHeight())
        return bufferedRow

    #Purpose: Returns an array of drawings buffered to the same given width
    def bufferToSameWidth(arrayOfDrawings, LRAlign, targetWidth):
        if type(arrayOfDrawings) is not list or \
           LRAlign not in ["center", "left", "right"] or \
           type(targetWidth) is not int:
            print("Error: parameter type mismatch in Drawing.bufferToSameWidth")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.bufferToSameWidth")
                return 1
        copyDrawings = copy.deepcopy(arrayOfDrawings)
        maxWidth = Drawing.getMaxWidth(copyDrawings)
        #buffer each image to the same height
        for i in range(0, len(copyDrawings)):
            #Note: Does not change height, so TBAlign is irrelevant and default to "center"
            copyDrawings[i].bufferAlign(LRAlign, "center", maxWidth, copyDrawings[i].getHeight()) 
        return copyDrawings

    #Purpose: Returns a drawing that is composed of 
    def combineIntoColumn(arrayOfDrawings, LRAlign, padding):
        if type(arrayOfDrawings) is not list or \
           LRAlign not in ["center", "left", "right"] or \
           type(padding) is not int:
            print("Error: parameter type mismatch in Drawing.combineIntoColumn")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.combineIntoColumn")
                return 1
        copyDrawings = copy.deepcopy(arrayOfDrawings)
        maxWidth = Drawing.getMaxWidth(copyDrawings)
        bufferedColumn = []
        #Buffer each image and add it to the column
        for i in range(0, len(copyDrawings)):
            copyDrawings[i].bufferAlign(LRAlign, "center", maxWidth, copyDrawings[i].getHeight())
            bufferedColumn.extend(copyDrawings[i].getDrawing())
            if padding > 0 and i != len(copyDrawings)-1:
                bufferedColumn += [" " * maxWidth] * padding
        return Drawing(bufferedColumn)

    #Purpose: Returns a column with each drawing buffered be spread equally over a given height
    def combineIntoColumnHeight(arrayOfDrawings, LRAlign, TBAlign, targetHeight):
        if type(arrayOfDrawings) is not list or \
           LRAlign not in ["center", "left", "right"] or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(targetHeight) is not int:
            print("Error: parameter type mismatch in Drawing.combineIntoColumnHeight")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                return Drawing([""])
        copyDrawings = copy.deepcopy(arrayOfDrawings)
        #figure out the total height of all the drawings being combined
        totalHeight = 0
        for i in range(0, len(copyDrawings)):
            totalHeight += copyDrawings[i].getHeight()
        #calculate how much each drawing gets buffered to fit the total height
        #Note: use this method of individual buffers to ensure that even if a large image is combined with a smaller one,
        # they are edited according to their individual sizes, not to a general width
        differenceInHeight = targetHeight - totalHeight
        individualBufferPadding = differenceInHeight/len(copyDrawings)
        #buffer each image to appropriate heights
        for j in range(0, len(copyDrawings)):
            copyDrawings[j].bufferAlign(LRAlign, TBAlign, copyDrawings[j].getWidth(), copyDrawings[j].getHeight() + int(individualBufferPadding))
        columnDrawing = Drawing.combineIntoColumn(copyDrawings, LRAlign, 0)
        columnDrawing.bufferAlign(LRAlign, TBAlign, columnDrawing.getWidth(), targetHeight)
        return columnDrawing

    #Purpose: Compresses 2 drawings side by side while removing excess whitespace between drawings
    def compressHorizontally(leftDrawing, rightDrawing, TBAlign, padding, targetHeight):
        if type(leftDrawing) is not Drawing or \
           type(rightDrawing) is not Drawing or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(padding) is not int or \
           type(targetHeight) is not int:
            print("Error: parameter type mismatch in Drawing.compressHorizontally")
            return 1
        #create copy/base for the upcoming edits
        bufferedDrawings = Drawing.bufferToSameHeight([copy.deepcopy(leftDrawing), copy.deepcopy(rightDrawing)], TBAlign, targetHeight)
        tempLeft = bufferedDrawings[0]
        tempRight = bufferedDrawings[1]

        #use to store the amount of whitespace that's allowed to be removed
        excessWhitespace = len(tempLeft.getDrawing()[0]) + len(tempRight.getDrawing()[0]) #sets excess whitespace to max possible length

        #find out how much whitespace to trim out from between images
        for i in range(0, tempLeft.getHeight()):
            totalLinesWS = tempLeft.numOfCharsInRowFromRight(i, " ") + tempRight.numOfCharsInRowFromLeft(i, " ")
            if totalLinesWS < excessWhitespace:
                    excessWhitespace = totalLinesWS

        #now remove the excess whitespace from each image
        compressed = []
        for i in range(0, tempLeft.getHeight()):  #iterate through each row of the drawing, from top to bottom
            tempValue = 0
            leftLine = tempLeft.getDrawing()[i]
            rightLine = tempRight.getDrawing()[i]
            while (tempValue < excessWhitespace-padding) and (leftLine[-1] == " "):
                #first remove as much as possible from left drawing
                leftLine = leftLine[:-1]
                tempValue += 1
            #if more still needs to be removed, take it from right drawing
            while (tempValue < excessWhitespace-padding) and (rightLine[0] == " "):
                rightLine = rightLine[1:]
                tempValue += 1
            #then add each line to the new drawing
            compressed.append(leftLine + rightLine)

        return Drawing(compressed)

    #Purpose: Compresses an array of drawings into a row while deleting excess whitespace between drawings
    def compressIntoRow(arrayOfDrawings, TBAlign, padding):
        if type(arrayOfDrawings) is not list or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(padding) is not int:
            print("Error: parameter type mismatch in Drawing.compressIntoRow")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                return Drawing([""])
        bufferedDrawings = Drawing.bufferToSameHeight(arrayOfDrawings, TBAlign, Drawing.getMaxHeight(arrayOfDrawings))
        while len(bufferedDrawings) > 2:
            bufferedDrawings = [Drawing.compressHorizontally(bufferedDrawings[0], bufferedDrawings[1]), \
                                TBAlign, padding, Drawing.getMaxHeight(bufferedDrawings)] \
                               + bufferedDrawings[2:]
        if len(bufferedDrawings) == 2:
            bufferedDrawings = Drawing.compressHorizontally(bufferedDrawings[0], bufferedDrawings[1], \
                                                            TBAlign, padding, Drawing.getMaxHeight(bufferedDrawings))
        return bufferedDrawings


    #Purpose: Compresses 2 drawings on top of eachother while removing excess whitespace between them
    #Note: BROKEN FOR NOW.  create overlaydrawings first
    def compressVertically(topDrawing, bottomDrawing, LRAlign, padding, targetWidth):
        if type(topDrawing) is not Drawing or \
           type(bottomDrawing) is not Drawing or \
           LRAlign not in ["center", "left", "right"] or \
           type(padding) is not int or \
           type(targetWidth) is not int:
            print("Error: parameter type mismatch in Drawing.compressVertically")
            return 1
        #create copy/base for the upcoming edits
        bufferedDrawings = Drawing.bufferToSameWidth([copy.deepcopy(topDrawing), copy.deepcopy(bottomDrawing)], LRAlign, targetWidth)
        tempTop = bufferedDrawings[0]
        tempBottom = bufferedDrawings[1]

        #use to store the amount of whitespace that's allowed to be removed
        excessWhitespace = tempTop.getHeight() + tempBottom.getHeight() #sets excess whitespace to max possible length

        #find out how much whitespace to trim out from between images
        for i in range(0, tempTop.getWidth()): #iterate over columns
            totalColumnsWS = tempTop.numOfCharsInColumnFromBottom(i, " ") + tempBottom.numOfCharsInColumnFromTop(i, " ")
            if totalColumnsWS < excessWhitespace:
                    excessWhitespace = totalColumnsWS

        #now remove the excess whitespace from each image by overlaying the bottom image over the top
        #Note: uses center because they are set to same width, and compressed vertically, so it shouldn't influence the drawing
        if excessWhitespace > 0:
            overlappedRows = Drawing.overlayDrawings(Drawing(tempTop.getDrawing()[-excessWhitespace:]), \
                                                     Drawing(tempBottom.getDrawing()[:excessWhitespace]), \
                                                     " ", "center", "center")

            compressed = []
            compressed.extend(tempTop.getDrawing()[:-excessWhitespace])
            compressed.extend(overlappedRows.getDrawing())
            compressed.extend(tempBottom.getDrawing()[excessWhitespace:])
        else:
            compressed = tempTop.getDrawing() + tempBottom.getDrawing()

        return Drawing(compressed)

    #Purpose: Compresses a series of images on top of eachother, eliminating excess whitespace between images, and stacks them from bottom up
    def compressIntoColumnFromBottomUp(arrayOfDrawings, LRAlign, padding, targetWidth):
        if type(arrayOfDrawings) is not list or \
           LRAlign not in ["center", "left", "right"] or \
           type(padding) is not int or \
           type(targetWidth) is not int:
            print("Error: parameter type mismatch in Drawing.compressIntoColumnFromBottomUp")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.compressIntoColumnFromBottomUp")
                return 1
        bufferedDrawings = Drawing.bufferToSameWidth(arrayOfDrawings, LRAlign, targetWidth)
        while len(bufferedDrawings) > 2:
            bufferedDrawings = [Drawing.compressVertically(bufferedDrawings[1], bufferedDrawings[0], LRAlign, padding, targetWidth)]\
                               + bufferedDrawings[2:]
        if len(bufferedDrawings) == 2:
            bufferedDrawings = Drawing.compressVertically(bufferedDrawings[1], bufferedDrawings[0], LRAlign, padding, targetWidth)
        return bufferedDrawings

    #Purpose: Compresses a series of images on top of eachother, eliminating excess whitespace between images, and stacks them from bottom up
    def compressIntoColumnFromTopDown(arrayOfDrawings, LRAlign, padding, targetWidth):
        if type(arrayOfDrawings) is not list or \
           LRAlign not in ["center", "left", "right"] or \
           type(padding) is not int or \
           type(targetWidth) is not int:
            print("Error: parameter type mismatch in Drawing.compressIntoColumnFromTopDown")
            return 1
        for e in range(0, len(arrayOfDrawings)):
            if type(arrayOfDrawings[e]) is not Drawing:
                print("Error: parameter type mismatch in Drawing.compressIntoColumnFromTopDown")
                return 1
        bufferedDrawings = Drawing.bufferToSameWidth(arrayOfDrawings, LRAlign, targetWidth)
        while len(bufferedDrawings) > 2:
            bufferedDrawings = [Drawing.compressVertically(bufferedDrawings[0], bufferedDrawings[1], LRAlign, padding, targetWidth)]\
                               + bufferedDrawings[2:]
        if len(bufferedDrawings) == 2:
            bufferedDrawings = Drawing.compressVertically(bufferedDrawings[0], bufferedDrawings[1], LRAlign, padding, targetWidth)
        return bufferedDrawings

    ##########################
    #Methods - Format Methods#
    ##########################
    #Methods related to the format required for the drawing.py file

    #Purpose: Takes a text file and converts it into a (series of) Drawings
    #Warning! For multiple drawings in a single file, make sure they are seperated by a simple new line with no other chars/whitespace
    #Warning! The txt file must be in the same directory as this library when used
    #Warning! Non-txt files are not supported
    def fileIntoDrawings(fileName):
        if type(fileName) is not str:
            print("Error: parameter type mismatch in Drawing.fileIntoDrawings")
            return 1
        if fileName.split(".")[-1] != "txt":
            return 1
        file = open(fileName, 'r')
        ASCIIart = file.read()
        file.close()
        #Split file up into "rows"
        rowFormat = ASCIIart.split("\n")
        #trim the preceding new lines
        while rowFormat[0] == "":
            rowFormat = rowFormat[1:]
        #distinguish between seperate drawings, and add them to a drawing array
        arrayOfDrawings = []
        tempPseudoDrawing = []
        for i in range(0, len(rowFormat)):
            if rowFormat[i] == "":
                arrayOfDrawings.append(Drawing(tempPseudoDrawing))
            else:
                tempPseudoDrawing.append(rowFormat[i])

        for drawing in arrayOfDrawings:
            drawing.bufferAlign("left", "center", drawing.getWidth(), drawing.getHeight())
            drawing.trim()
            drawing.setOriginal(drawing.getDrawing())
            
        return arrayOfDrawings
    
    #Purpose: Takes a Drawing object and prints to screen the format required for the drawing file
    def returnInFormat(self, drawingName):
        if type(drawingName) is not str:
            return 1
        
        #add the name and initial bracketting
        drawing = []
        drawing.append(str(drawingName) + " = [")

        #add string quotes around each ascii art line, complete with comma for the list
        for row in self.getDrawing():

            #add extra \'s to avoid trigger commands (dunno what they;re called)
            if row[-1] == "\\":
                row += "\\"
                    
            drawing.append('\t"' + row + '",')

        #remove the last comma from last element
        lastRow = drawing[len(drawing)-1]
        drawing[len(drawing)-1] = lastRow[:-1]

        #add final bracket, complete with a tab
        drawing.append("\t]")

        return drawing

    #Purpose: Saves multiple (or a single element list of) drawings onto the end of drawings.py file
    #Note: If autoFormat is True, then it will automatically format it in proper "dCamelCaseName", where d stands for Drawing
    def saveMultipleDrawings(arrayOfDrawings, nameOfDrawing, autoFormatBoolean):
        if type(nameOfDrawing) is not str or \
           type(autoFormatBoolean) is not bool or\
           type(arrayOfDrawings) is not list:
            print("Error: parameter type mismatch in Drawing.saveMultipleDrawings")
            return 1
        for drawing in arrayOfDrawings:
            if type(drawing) is not Drawing:
                print("Error: parameter type mismatch in Drawing.saveMultipleDrawings")
                return 1
            
        copyArray = copy.deepcopy(arrayOfDrawings)
        copyName = copy.deepcopy(nameOfDrawing)

        #format the name to make sure it can be used as a variable name
        if autoFormatBoolean:
            copyName = copyName.split()
            for i in range(0, len(copyName)):
                copyName[i] = copyName[i].capitalize()
            copyName = ["d"] + copyName
            copyName = "".join(copyName)

        #Remove non-variable friendly characters
        alpha = string.ascii_letters
        i = 0
        while i < len(copyName):
            if copyName[i] not in alpha:
                copyName = copyName[:i] + copyName[i+1:]
            else:
                i += 1

        #Format the drawings
        for j in range(0, len(copyArray)):
            copyArray[j] = copyArray[j].returnInFormat(copyName+str(j+1))
        
        #Open the file and save drawing
        file = open("drawings.py", 'a')
        for k in range(0, len(copyArray)):
            tempDrawing = copyArray[k]
            for l in range(0, len(tempDrawing)):
                file.write(tempDrawing[l] + "\n")
            file.write("\n")

        file.close()
        return 0
        

    #Purpose: Takes a drawing, returns the drawing after being flipped horizontally
    #Warning! Best to save the new image after manually checking it first, as not all characters are flippable (D, G, 3, etc...)
    def flipHorizontally(drawing):
        if type(drawing) is not Drawing:
            return 1
        #get the original image to be flipped
        flippedImage = copy.deepcopy(drawing.getDrawing())

        #iterate through each row, and then each char in row, and flip the characters and order
        for i in range(0, len(flippedImage)):
            flippedImage[i] = Drawing.flipRow(flippedImage[i])

        #print the new drawing
        completedDrawing = Drawing(flippedImage)
        return completedDrawing

    #Purpose: Takes a string (a row of a drawing), reverses the order and flips each image to a mirrored counterpart
    def flipRow(string):
        if type(string) is not str:
            return 1
        flippedRow = ""
        #iterate through the original row, adding them to the final product in reverse order
        for i in range(len(string)-1, -1, -1):
            #uses flipChar to flip each individual character of the string
            flippedRow += Drawing.flipChar(string[i])
        return flippedRow

    #Purpose: Takes a char, and returns the flipped version if it has one (if not, the original char is returned)
    def flipChar(char):
        if type(char) is not str or \
           len(char) != 1:
            return 1

        #use switch-case to find a reversable char
        if char == "/":
            return "\\"
        elif char == "\\":
            return "/"
        
        elif char == "(":
            return ")"
        elif char == ")":
            return "("
        
        elif char == "d":
            return "b"
        elif char == "b":
            return "d"
        
        elif char == "<":
            return ">"
        elif char == ">":
            return "<"
        
        elif char == "[":
            return "]"
        elif char == "]":
            return "["
        
        elif char == "{":
            return "}"
        elif char == "}":
            return "{"
        
        #if char was not reversable, return the original char
        return char

        

##############################
###Classes - Jigsaw Drawing###
##############################
#Purpose: Combines a Jigsaw Base and array of Jigsaw Pieces to create a complete (dynamic) Drawing Object
class Jigsaw(Drawing):
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########
    #Note: remember it inherets _drawing and _original
    #_drawing/_original will be the useable "compiled" drawings so that they can use all the Drawing methods as well
    #Note: The following members are used by the class to compile the useable Drawing, and should not be displayed/modified as Drawings
    #Note: The index of the pieces array should correspond with the appropriate anchorpoint in base as to where it should be able to attach to
    _base = [] #type: JigsawBase
    _pieces = [] #type: Array of JigsawPieces

    ########################
    #Methods - Init/Set/Get#
    ########################

    def __init__(self, newBase, newPieces):
        if type(newBase) is not JigsawBase or \
           type(newPieces) is not list:
            print("Error: parameter type mismatch in Jigsaw.__init__()")
            self._base = JigsawBase("", [])
            self._pieces = []
            return 1
        for piece in newPieces:
            if type(piece) is not JigsawPiece:
                print("Error: parameter type mismatch in Jigsaw.__init__()")
                return 1
        self._base = copy.deepcopy(newBase)
        self._pieces = copy.deepcopy(newPieces)
        self.assembleJigsawDrawing()
        super().__init__(self.getDrawing())
        return

    def getBase(self):
        return self._base

    def getPieces(self):
        return self._pieces

    def setBase(self, newBase):
        if type(newBase) is not JigsawBase:
            print("Error: parameter type mismatch in Jigsaw.setBase()")
            return 1
        self._base = copy.deepcopy(newBase)

    def setPiece(self, singlePiece, index):
        if type(singlePiece) is not JigsawPiece or \
           type(index) is not int or \
           index >= len(self._pieces) or \
           index < 0:
            print("Error: parameter type mismatch in Jigsaw.setBase()")
            return 1
        self._pieces[index] = copy.deepcopy(singlePiece)
        
    #takes two pieces that were created as 'puzzle piece' and sticks them together
    #note: the first line of a 'puzzle piece' type drawing is a single char, this is where the joint between images will be
    #note: the second line of a pp drawing is a single char, denoting what the joint-char should be replaced with ("", " ", "/", etcc)
    #the first piece will be considered the base, and the second will be laid overtop
    def assembleJigsawDrawing(self):
        base = copy.deepcopy(self.getBase())

        for i in range(0, len(base.getAnchorPoints())):
            #prep both pieces
            overlay = copy.deepcopy(self.getPieces()[i])
            #make base big enough to accomodate the new piece
            base.bufferAlign("center", "center", base.getWidth()+(2*overlay.getWidth()), base.getHeight()+(2*overlay.getHeight()))

            #find overlays joint and make the mend 
            overlaysJointCoord = overlay.getCoordOfChar(overlay.getJoint(), 1)
            mendedOverlay = Drawing(overlay.getMendedDrawing())
            del overlay
            #find bases joint and record it for later
            basesJointCoord = base.getCoordOfChar(base.getAnchorPoints()[i], 1)

            #overlay the two pieces
            #must buffer the overlay so that it's joint is in the same column as the bases, without regard to overall width
            #  math:   length of original overlay + difference of the 2 column index * 2 <- x2 because it must add the difference to both side of the drawing
            mendedOverlay.bufferAlign("center", "center", mendedOverlay.getWidth()+(basesJointCoord[0]-overlaysJointCoord[0])*2, mendedOverlay.getHeight())
            # then buffer to base's width to remove excess on the overlays right side
            mendedOverlay.bufferAlign("left", "center", base.getWidth(), mendedOverlay.getHeight())

            #now find the area of the base that will need to be overlayed
            spliceRange = [basesJointCoord[1]-overlaysJointCoord[1], basesJointCoord[1]+mendedOverlay.getHeight()-overlaysJointCoord[1]]
            baseSplice = Drawing(base.getDrawing()[spliceRange[0]:spliceRange[1]])
            overlayedSplice = Drawing.overlayDrawings(baseSplice, mendedOverlay, " ", "center", "center")
            del mendedOverlay
            del baseSplice

            #put the now combined rows back into their proper place in the base
            fullDrawing = Drawing(base.getDrawing()[:spliceRange[0]] + overlayedSplice.getDrawing() + base.getDrawing()[spliceRange[1]:])
            #trim all excess whitespace before returning final product
            fullDrawing.trim()
            base.setDrawing(fullDrawing.getDrawing())
            del fullDrawing

        #Assign the new drawing to the _drawing variable
        self.setDrawing(base.getDrawing())
        return 0


###########################
###Classes - Jigsaw Base###
###########################
#Purpose: Acts as the base to the jigsaw drawing and stores info for attaching pieces
class JigsawBase(Drawing):
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########
    #Note: remember it inherets _drawing and _original
    #_drawing/_original will be the useable "base" components for this class
    _arrayOfAnchorPoints = [] #Each anchor point is a single-element string that denotes what character in the drawing should be used to attach a JigsawPiece

    ########################
    #Methods - Init/Set/Get#
    ########################

    #Note: Will default the init method if any of the anchor points appear more/less than once in a given base
    def __init__(self, basePseudoDrawing, anchorPoints):
        if type(basePseudoDrawing) is not list or\
           type(anchorPoints) is not list:
            print("Error: parameter type mismatch in JigsawBase __init__()")
            return 1
        for anchor in anchorPoints:
            if type(anchor) is not str or\
               len(anchor) != 1:
                print("Error: parameter type mismatch in JigsawBase __init__()")
                return 1
        #Calculate how many of each anchor point are in the pseudodrawing, and only procede if there is only 1 of each anchor point    
        count = [0] * len(anchorPoints) #each element in count refers to the relative element in anchor points
        for row in basePseudoDrawing:
            for character in row:
                for i in range(0, len(anchorPoints)):
                    if character == anchorPoints[i]:
                        count[i] += 1
        #now check to make sure each element in count is 1
        for element in count:
            if element != 1:
                print("Error: Incorrect number of instances of an anchor point (only 1 instance allowed)")
                return 1

        super().__init__(basePseudoDrawing)
        self._arrayOfAnchorPoints = copy.deepcopy(anchorPoints)

    #Purpose: Act as secondary constructor for formatted drawings where first element is the anchorPoints array, and rest is the drawing
    def initFromFormattedJBDrawing(formattedDrawing):
        if type(formattedDrawing) is not list or \
           type(formattedDrawing[0]) is not list:
            print("Error: parameter type mismatch in JigsawBase.initFromFormattedJBDrawing")
            return 1
        for anchor in formattedDrawing[0]:
            if type(anchor) is not str or\
               len(anchor) != 1:
                print("Error: parameter type mismatch in JigsawBase.initFromFormattedJBDrawing")
                return 1
        return JigsawBase(formattedDrawing[1:], formattedDrawing[0])
        
    def getAnchorPoints(self):
        return self._arrayOfAnchorPoints

    def setAnchorPoints(self, anchors):
        if type(anchors) is not list:
            print("Error: parameter type mismatch in JigsawBase.setAnchorPoints()")
            return 1
        for a in anchors:
            if type(a) is not str or \
               len(a) != 1:
                print("Error: parameter type mismatch in JigsawBase.setAnchorPoints()")
                return 1
        self._arrayOfAnchorPoints = anchors


############################
###Classes - Jigsaw Piece###
############################
#Purpose: Acts as a single piece to the jigsaw drawing and stores info for joints and mends
class JigsawPiece(Drawing):
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########
    #Note: remember it inherets _drawing and _original
    #_drawing/_original will be the useable "base" components for this class
    _joint = "" #the single char string that shows where the piece should be attached
    _mend = "" #the single char string that replaces the _joint after being attached
    _attachToBaseIndexNum = -1 #Used for pieces that can only be attached to a certain anchor index of a JigsawBase

    ########################
    #Methods - Init/Set/Get#
    ########################

    def __init__(self, pseudoDrawing, joint, mend):
        if type(pseudoDrawing) is not list or\
           type(joint) is not str or \
           len(joint) != 1 or \
           type(mend) is not str or \
           len(mend) != 1:
            print("Error: parameter type mismatch in JigsawPiece.__init__()")
            return 1
        for row in pseudoDrawing:
            if type(row) is not str:
                print("Error: parameter type mismatch in JigsawPiece.__init__()")
                return 1
        self._joint = joint
        self._mend = mend
        super().__init__(pseudoDrawing)

    #Purpose: Act as secondary constructor for a formatted drawings where first element is the anchor/joint, second is the mend, and rest is the drawing
    def initFromFormattedJPDrawing(formattedDrawing):
        if type(formattedDrawing) is not list or\
           len(formattedDrawing) < 3 or \
           type(formattedDrawing[0]) is not str or \
           len(formattedDrawing[0]) != 1 or \
           type(formattedDrawing[1]) is not str or \
           len(formattedDrawing[1]) != 1:
            print("Error: parameter type mismatch in JigsawPiece.initFromFormattedJPDrawing")
            return 1
        for row in formattedDrawing:
            if type(row) is not str:
                print("Error: parameter type mismatch in JigsawPiece.initFromFormattedJPDrawing")
                return 1
        return JigsawPiece(formattedDrawing[2:], formattedDrawing[0], formattedDrawing[1])

    def getJoint(self):
        return self._joint

    def getMend(self):
        return self._mend

    #Purpose: returns the pseudo-drawing after the mend has replaced the joint char on the JP drawing
    def getMendedDrawing(self):
        tempDrawing = copy.deepcopy(self.getDrawing())
        for i in range(0, len(tempDrawing)): #iterate over rows
            tempRow = tempDrawing[i]
            for j in range(0, len(tempRow)): #iterate over chars in row
                if tempRow[j] == self.getJoint():
                    tempRow = tempRow[:j] + self.getMend() + tempRow[j+1:]
                    return (tempDrawing[:i] + [tempRow] + tempDrawing[i+1:])
        return 1 #getting here means the mend was not found/fixed, so return error

    def setPrefferedAnchorIndex(self, anchorIndex):
        if type(anchorIndex) is not int:
            print("Error: parameter type mismatch in JigsawPiece.setPrefferedAnchorIndex")
            return 1
        self._attachToBaseIndexNum = anchorIndex
        return
        
    def getPrefferedAnchorIndex(self):
        return self._attachToBaseIndexNum
            


##########################
###Classes - Text Field###
##########################

#Purpose: A special type of drawing that accounts for text wrapping and alignment
class TextField(Drawing):
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########

    _paragraphs = []  

    ########################
    #Methods - Init/Set/Get#
    ########################

    def __init__(self, arrayOfParagraphs):
        if type(arrayOfParagraphs) is not list:
            return 1
        for item in arrayOfParagraphs:
            if type(item) is not str:
                return 1
        self._paragraphs = arrayOfParagraphs
        return

    ##############################################
    #Methods - Instance Methods - Modifying Text #
    ##############################################
    #Directly modifies the paragraphs to simulate certain text effects

    #Purpose: Indents each paragraph by a certain number of spaces
    #def addIndentation(self, numOfSpacesToIndent):
        
    #Purpose: Removes indentation (no matter how many spaces it's been indented)
    #def removeIndentation(self)
    
    #Purpose: Add Basic single-char bullet points to each paragraph
    #def addBasicBullets(self, bulletChar, indentationBetweenNumAndText):
        
    #Purpose: Removes basic single-char bullet points and all subsequent indentation before the paragraph
    #def removeBasicBullets(self):

    #Purpose: Adds numbering to each paragraph, starting at a starting number, incrementing by a certain value each time, and followed by a char (possibly bracket or period) and indentation
    #def addNumbering(self, startingNumber, numberIncrementation, charAfterNumber, indentationBetweenNumAndText):

    #Purpose: Removes the numbering from each paragraph
    #Warning! Will remove all starting chars that are integers, and the character afterword so long as its not whitespace, then removes indentation

        
    #######################################
    #Methods - Class Methods - Formatting #
    #######################################

    #Purpose: Converts the paragraphs into Drawing object that's formatted with a certain alignment
    def formatParagraph(paragraphs, targetWidth, LRAlign):
        if type(targetWidth) is not int or \
           type(paragraphs) is not TextField or \
           type(LRAlign) is not str or \
           LRAlign not in ["center", "left", "right"]:
            return 1
        
        formattedLines = []
        indexTracker = 0
        offset = 0

        #iterate through each paragraph in the array
        for i in range(0, len(paragraphs._paragraphs)):
            indexTracker = 0
            offset = 0
            tempParagraph = paragraphs._paragraphs[i]
            #provided the text is wider than the target width, start at targetWidth index, the decrement til a space is found
            while (len(tempParagraph)-indexTracker) > targetWidth:
                offset = 0 #use the offset to find the nearest break in the sentence to create a 'new line'
                #Note: indexTracker keeps the position of the start of the next new line in the original paragraph
                while tempParagraph[indexTracker+targetWidth-offset] != ' ':
                    offset += 1
                formattedLines.append(tempParagraph[indexTracker:indexTracker+targetWidth-offset])
                indexTracker += targetWidth-offset+1 #+1 to make sure the " " isn't added onto the front of the next line
            # take the left over bit and add it
            formattedLines.append(tempParagraph[indexTracker:])

        formattedLines = Drawing(formattedLines)
        formattedLines.bufferAlign(LRAlign, "center", formattedLines.getWidth(), formattedLines.getHeight())
        return formattedLines

    #Purpose: Converts the paragraphs into Drawing object that's formatted to appear as a list of options
    #           Priority goes to filling a certain number of options in a row before proceeding to next row
    def formatOptionsIntoRows(options, numOfColumns, targetWidth, LRAlign):
        if type(numOfColumns) is not int or \
           type(targetWidth) is not int or \
           type(options) is not TextField or \
           LRAlign not in ["center", "left", "right"]:
            return 1

        widthPerColumn = int(targetWidth/numOfColumns)

        #split up the original list of options into separate lists: each list is a single column
        columns = []
        for i in range(0, numOfColumns):
            columns.append(copy.deepcopy(Drawing([])))
            
        #print("TEST: id(columns[0]):"+str(id(columns[0])))
        #print("TEST: id(columns[1]):"+str(id(columns[1])))
        

        #iterate through all the options and add them to the appropriate column
        for i in range(0, len(options._paragraphs)):
            columns[i%numOfColumns]._drawing.append(options._paragraphs[i])
            #print("TEST: i%numOfColumns: "+str(i%numOfColumns)+", i:"+str(i),", numOfColumns:"+str(numOfColumns))

        #iterate through each column and buffer it accordingly
        for column in columns:
            column.bufferAlign(LRAlign, "center", widthPerColumn, column.getHeight())

        #combine all columns into row
        return Drawing.combineIntoRow(columns, "top", 0)

    #Purpose: implements formatOptionsIntoRows but with a title above the options
    def formatOptionsIntoRowsWithTitle(options, numOfColumns, targetWidth, LRAlign, title, titleAlign):
        if type(numOfColumns) is not int or \
           type(targetWidth) is not int or \
           type(options) is not TextField or \
           LRAlign not in ["center", "left", "right"]or \
           type(title) is not TextField or \
           titleAlign not in ["center", "left", "right"]:
            return 1

        titleDrawing = TextField.formatParagraph(title, targetWidth, titleAlign)
        optionsDrawing = TextField.formatOptionsIntoRows(options, numOfColumns, targetWidth, LRAlign)

        #print("TEST: type(titleDrawing):"+str(type(titleDrawing))+", type(optionsDrawing):"+str(type(optionsDrawing)))

        return Drawing.combineIntoColumn([titleDrawing, optionsDrawing], titleAlign, 0)
    
    #Purpose: Returns a Drawing that uses another drawing as a bullet point to each paragraph
    #def formatWithDrawingBullets(textField, bulletDrawing, LRAlign, TBAlign, targetWidth, indentationBetweenBulletAndText, paddingBetweenBullets):



######################
###Classes - Border###
######################

#Purpose: A class to store information about a "border" and provide proper methods to modify the information
#Note: A border is a simple 1-char-width edge added to the outside of a drawing
class Border:
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########
    
    _corners = [" ", " ", " ", " "]
    _borders = [" ", " ", " ", " "]  

    ########################
    #Methods - Init/Set/Get#
    ########################

    def __init__(self, arrayOfCorners, arrayOfBorders):
        self._corners = [" ", " ", " ", " "]
        self._borders = [" ", " ", " ", " "]
        #run through a check to make sure each array is formatted correctly and each entry is a char, not string
        if len(arrayOfCorners) == 4 and len(arrayOfBorders) == 4:
            for i in range(0, 4):
                if (type(arrayOfCorners[i]) is str) and (len(arrayOfCorners[i]) == 1) and \
                   (type(arrayOfBorders[i]) is str) and (len(arrayOfBorders[i]) == 1):
                    self._corners[i] = arrayOfCorners[i]
                    self._borders[i] = arrayOfBorders[i]

    def getCorners(self):
        return self._corners

    def setCorners(self, arrayOfCorners):
        if type(arrayOfBorders) is not list:
            return 1
        if len(arrayOfCorners) == 4:
            for i in range(0, 4):
                if (type(arrayOfCorners[i]) is not str) or (len(arrayOfCorners[i]) != 1):
                    return 1
        else:
            return 1
        self._corners = arrayOfCorners
        return 0
    
    def getBorders(self):
        return self._borders

    def setBorders(self, arrayOfBorders):
        if type(arrayOfBorders) is not list:
            return 1
        if len(arrayOfBorders) == 4:
            for i in range(0, 4):
                if (type(arrayOfBorders[i]) is not str) or (len(arrayOfBorders[i]) != 1):
                    return 1
        else:
            return 1
        self._borders = arrayOfBorders
        return 0





######################
###Classes - Frames###
######################

#Purpose: A class to store information about a "frame" and provide proper methods to modify the information
#Note: A frame is a more elaborate version of a border that makes use of other drawings instead of single chars
class Frame:
    #Note: Anything that starts with an _ should be treated as private
    
    #########
    #Members#
    #########
    
    _topDrawing = []
    _leftDrawing = []
    _rightDrawing = []
    _bottomDrawing = []
    _topAlign = "center"
    _leftAlign = "center"
    _rightAlign = "center"
    _bottomAlign = "center"
    _topRepeat = False
    _leftRepeat = False
    _rightRepeat = False
    _bottomRepeat = False

    ########################
    #Methods - Init/Set/Get#
    ########################

    def __init__(self, top, left, right, bottom):
        if type(top) is not Drawing or \
           type(left) is not Drawing or \
           type(right) is not Drawing or \
           type(bottom) is not Drawing:
            return 1
        self._topDrawing = top
        self._leftDrawing = left
        self._rightDrawing = right
        self._bottomDrawing = bottom

    def getTop(self):
        return self._topDrawing

    def getLeft(self):
        return self._leftDrawing

    def getRight(self):
        return self._rightDrawing

    def getBottom(self):
        return self._bottomDrawing

    def getTopAlign(self):
        return self._topAlign

    def getLeftAlign(self):
        return self._leftAlign

    def getRightAlign(self):
        return self._rightAlign

    def getBottomAlign(self):
        return self._bottomAlign

    def getTopRepeat(self):
        return self._topRepeat

    def getLeftRepeat(self):
        return self._leftRepeat

    def getRightRepeat(self):
        return self._rightRepeat

    def getBottomRepeat(self):
        return self._bottomRepeat

    def setTop(self, drawing):
        if type(drawing) is not Drawing:
            return 1
        _topDrawing = copy.deepcopy(drawing)
        return 0

    def setLeft(self, drawing):
        if type(drawing) is not Drawing:
            return 1
        _leftDrawing = copy.deepcopy(drawing)
        return 0

    def setRight(self, drawing):
        if type(drawing) is not Drawing:
            return 1
        _rightDrawing = copy.deepcopy(drawing)
        return 0

    def setBottom(self, drawing):
        if type(drawing) is not Drawing:
            return 1
        _bottomDrawing = copy.deepcopy(drawing)
        return 0

    def setTopAlign(self, string):
        if type(string) is not str:
            return 1
        self._topAlign = string
        return 0

    def setLeftAlign(self, string):
        if type(string) is not str:
            return 1
        self._leftAlign = string
        return 0

    def setRightAlign(self, string):
        if type(string) is not str:
            return 1
        self._rightAlign = string
        return 0

    def setBottomAlign(self, string):
        if type(string) is not str:
            return 1
        self._bottomAlign = string
        return 0

    def setAlignments(self, top, left, right, bottom):
        if type(top) is not str or\
           type(left) is not str or\
           type(right) is not str or\
           type(bottom) is not str:
            return 1
        self._topAlign = top
        self._leftAlign = left
        self._rightAlign = right
        self._bottomAlign = bottom
        return 0

    def setTopRepeat(self, boolean):
        if type(boolean) is not bool:
            return 1
        self._topRepeat = boolean
        return 0

    def setLeftRepeat(self, boolean):
        if type(boolean) is not bool:
            return 1
        self._leftRepeat = boolean
        return 0

    def setRightRepeat(self, boolean):
        if type(boolean) is not bool:
            return 1
        self._rightRepeat = boolean
        return 0

    def setBottomRepeat(self, boolean):
        if type(boolean) is not bool:
            return 1
        self._bottomRepeat = boolean
        return 0

    def setRepeats(self, top, left, right, bottom):
        if type(top) is not bool or\
           type(left) is not bool or\
           type(right) is not bool or\
           type(bottom) is not bool:
            return 1
        self._topRepeat = top
        self._leftRepeat = left
        self._rightRepeat = right
        self._bottomRepeat = bottom
        return 0
        
    ##########################################
    #Methods - Instance Methods - Generators #
    ##########################################
    #These methods call upon the instance info to generate parts of the Frame for the final piece
   
    #Purpose: Generates the left border drawing by taking into account repetition and alignment
    def generateLeftBorder(self, targetHeight):
        if type(targetWidth) is int:
            #Calculate the number of side-frames are required to fully enclose the image, if border repeats
            if self.getLeftRepeat() == True:
                #Note: the [1] is to grab the returning value that corresponds to the height value (check howManyCanFit method)
                #Note: +2 will ensure that when buffered, if center-aligned, it won't create weird images if they fit perfectly to begin with
                numOfLeftBorders = self.getLeft().howManyCanFit(self.getLeft().getWidth(), targetHeight)[1]+2

                #Now create the side borders, and buffer those with the center to create a row
                leftBorder = Drawing.combineIntoColumn([self.getLeft()]*numOfLeftBorders, "center", 0)
                leftBorder.bufferAlign("center", self.getLeftAlign(), leftBorder.getWidth(), targetHeight)
            else:
                leftBorder = copy.deepcopy(self.getLeft())
                leftBorder.bufferAlign("center", self.getLeftAlign(), self.getLeft().getWidth(), targetHeight)
            return leftBorder
        else:
            return Drawing([""])
        
    #Purpose: Generates the right border drawing by taking into account repetition and alignment
    def generateRightBorder(self, targetHeight):
        if type(targetWidth) is int:
            #Calculate the number of side-frames are required to fully enclose the image, if border repeats
            if self.getRightRepeat() == True:
                #Note: the [1] is to grab the returning value that corresponds to the height value (check howManyCanFit method)
                #Note: +2 will ensure that when buffered, if center-aligned, it won't create weird images if they fit perfectly to begin with
                numOfRightBorders = self.getRight().howManyCanFit(self.getRight().getWidth(), targetHeight)[1]+2

                #Now create the side borders, and buffer those with the center to create a row
                rightBorder = Drawing.combineIntoColumn([self.getRight()]*numOfRightBorders, "center", 0)
                rightBorder.bufferAlign("center", self.getRightAlign(), rightBorder.getWidth(), targetHeight)
            else:
                rightBorder = copy.deepcopy(self.getRight())
                rightBorder.bufferAlign("center", self.getRightAlign(), self.getRight().getWidth(), targetHeight)
            return rightBorder
        else:
            return Drawing([""])
        
    #Purpose: Generates the left border drawing by taking into account repetition and alignment
    def generateTopBorder(self, targetWidth):
        if type(targetWidth) is int:
            #Calculate the number of side-frames are required to fully enclose the image, if border repeats
            if self.getTopRepeat() == True:
                #Note: the [1] is to grab the returning value that corresponds to the height value (check howManyCanFit method)
                #Note: +2 will ensure that when buffered, if center-aligned, it won't create weird images if they fit perfectly to begin with
                numOfTopBorders = self.getTop().howManyCanFit(targetWidth, self.getTop().getHeight())[0]+2

                #Now create the side borders, and buffer those with the center to create a row
                topBorder = Drawing.combineIntoRow([self.getTop()]*numOfTopBorders, "center", 0)
                topBorder.bufferAlign("center", self.getTopAlign(), targetWidth, topBorder.getHeight())
            else:
                topBorder = copy.deepcopy(self.getTop())
                topBorder.bufferAlign(self.getTopAlign(), "center", targetWidth, self.getTop().getHeight())
            return topBorder
        else:
            return Drawing([""])
        
    #Purpose: Generates the left border drawing by taking into account repetition and alignment
    def generateBottomBorder(self, targetWidth):
        if type(targetWidth) is int:
            #Calculate the number of side-frames are required to fully enclose the image, if border repeats
            if self.getBottomRepeat() == True:
                #Note: the [1] is to grab the returning value that corresponds to the height value (check howManyCanFit method)
                #Note: +2 will ensure that when buffered, if center-aligned, it won't create weird images if they fit perfectly to begin with
                numOfBottomBorders = self.getBottom().howManyCanFit(targetWidth, self.getBottom().getHeight())[0]+2

                #Now create the side borders, and buffer those with the center to create a row
                bottomBorder = Drawing.combineIntoRow([self.getBottom()]*numOfBottomBorders, "center", 0)
                bottomBorder.bufferAlign("center", self.getBottomAlign(), targetWidth, bottomBorder.getHeight())
            else:
                bottomBorder = copy.deepcopy(self.getBottom())
                bottomBorder.bufferAlign(self.getBottomAlign(), "center", targetWidth, self.getBottom().getHeight())
            return bottomBorder
        else:
            return Drawing([""])



    #########################
    #Methods - Class Methods#
    #########################
    #These classes are meant to be used to return new values/drawings, and should not be called by an object instance
    
    #Purpose: Frames a drawing with a given Frame object, with a certain amount of padding in between the two
    #Note: This is a class method as opposed to instance method because it is not as easy to reverse as a regular Border
    def addFrameToDrawing(drawing, frame, LRAlign, TBAlign, padding):
        #Do a type check and return 1 for error
        if type(drawing) is not Drawing or \
           type(frame) is not Frame or \
           LRAlign not in ["center", "left", "right"] or \
           TBAlign not in ["center", "top", "bottom"] or \
           type(padding) is not int:
            return 1
        
        #Buffer the center image to account for padding
        center = copy.deepcopy(drawing)
        center.bufferAlign("center", "center", center.getWidth()+(padding*2), center.getHeight()+(padding*2))

        #Get each of the Individual drawings of the frame
        centerDrawingBasedWidth = center.getWidth() + frame.getLeft().getWidth()+ frame.getRight().getWidth()
        frameBasedWidth = max([frame.getTop().getWidth(), frame.getBottom().getWidth()])
        minimumWidth = max([centerDrawingBasedWidth, frameBasedWidth])
        top = frame.generateTopBorder(minimumWidth)
        left = frame.generateLeftBorder(center.getHeight())
        right = frame.generateRightBorder(center.getHeight())
        bottom = frame.generateBottomBorder(minimumWidth)
        
        #Calculate how much space needs to be added (if any) to the sides of the center image to balance the width of the final image
        extraSpace = minimumWidth - (center.getWidth() + left.getWidth() + right.getWidth())
        if extraSpace > 0:
            center.bufferAlign(LRAlign, TBAlign, center.getWidth()+extraSpace, center.getHeight())


        #Now create the side borders, and buffer those with the center to create a row
        middleSection = Drawing.combineIntoRow([left, center, right], TBAlign, 0)

        #Finally add all three pieces together
        return Drawing.combineIntoColumn([top, middleSection, bottom], "center", 0)

    

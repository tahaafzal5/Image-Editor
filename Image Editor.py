import graphics
from tkinter.filedialog import asksaveasfilename as save


# opens the image user wants, opens a graphical window, and draws the image on it leaving out space for the button-bar
def openImageAndWindow(imgName):
    img = graphics.Image(graphics.Point(0, 0), imgName)
    width = img.getWidth()
    height = img.getHeight()
    img.move(width//2, height//2)
    win = graphics.GraphWin(imgName, width, height + 50)
    img.move(0, 50)
    img.draw(win)
    
    # call drawButtons to draw the buttons on window
    drawButtons(win)
    
    # return values for image and window
    return img, win


# draws all 4 buttons on the button bar along with text displayed on them
def drawButtons(win):
    buttonStats = graphics.Rectangle(graphics.Point(18, 12), graphics.Point(100, 35)).draw(win)
    textStats = graphics.Text(graphics.Point(59, 23.5), "Stats").draw(win)

    buttonGrayscale = graphics.Rectangle(graphics.Point(120, 12), graphics.Point(202, 35)).draw(win)
    textGrayscale = graphics.Text(graphics.Point(161, 23.5), "Grayscale").draw(win)

    buttonNegative = graphics.Rectangle(graphics.Point(222, 12), graphics.Point(304, 35)).draw(win)
    textNegative = graphics.Text(graphics.Point(263, 23.5), "Negative").draw(win)

    buttonQuit = buttonNegative.clone()
    buttonQuit.move(102, 0)
    buttonQuit.draw(win)
    textQuit = graphics.Text(graphics.Point(365, 23.5), "Quit").draw(win)


# converts the image into grayscale
def convertGrayscale(imgName, img, win):
    print("Converting", imgName, "to grayscale...")
    for col in range(img.getHeight()):
        for row in range(img.getWidth()):
            r, g, b = img.getPixel(row, col)
            brightness = int(round((0.299*r + 0.587*g + 0.114*b), 2))
            img.setPixel(row, col, graphics.color_rgb(brightness, brightness, brightness))
        win.update()
    # tells user that action is complete
    print("Done.")


# converts the image to its negative, used again to convert it back from negative
def convertNegative(imgName, img, win):
    
    # lets user know the process has started
    print("Converting", imgName, "to negative...")
    
    # changes pixel color by row and column by a value of 255 which results in the opposite
    for col in range(img.getHeight()):
        for row in range(img.getWidth()):
            r, g, b = img.getPixel(row, col)
            img.setPixel(row, col, graphics.color_rgb(255 - r, 255 - g, 255 - b))
        win.update()
    
    # tells user that the action is complete
    print("Done.")


# outputs image stats
def stats(img):
    
    # introduces function and sets empty lists
    print("Calculating image stats...")
    redList = []
    greenList =[]
    blueList =[]
    
    # adds 0's to each list so that there are correct number of values
    for i in range(0, 256):
        redList.append(0)
        greenList.append(0)
        blueList.append(0)
    
    # takes each pixel color value by row and column
    for col in range(img.getHeight()):
        for row in range(img.getWidth()):
            r, g, b = img.getPixel(row, col)
            
            # accumulators keep track of running totals
            redList[r] = redList[r] + 1
            greenList[g] = greenList[g] + 1
            blueList[b] = blueList[b] + 1
    
    # set value for total which will be used to calculate mean
    totalr = 0
    totalg = 0
    totalb = 0
    
    # find total values for red, green, and blue
    for i in range(0, 256):
        totalr = i*redList[i] + totalr
        totalg = i*greenList[i] + totalg
        totalb = i*blueList[i] + totalb
    
    # calculate mean using total color values and total pixel count
    meanr = totalr/((img.getHeight())*(img.getWidth()))
    meang = totalg/((img.getHeight())*(img.getWidth()))
    meanb = totalb/((img.getHeight())*(img.getWidth()))
    
    # print results
    print("Mean red", meanr)
    print("Mean green", meang)
    print("Mean blue", meanb)
    print("Total number of pixels:", (img.getHeight())*(img.getWidth()))
    print("  Red  Green  Blue")

    for i in range(0, 256):
        print(i, redList[i], greenList[i], blueList[i])
    
    print("Done.")


# decides which function to call based on the button clicks
def handleClick(click, imgName, img, win):

    xClick = click.getX()
    yClick = click.getY()
    
    # sets loop that splits button clicks based on where they occured, calls corresponding functions
    if xClick >= 120 and xClick <= 202 and yClick >= 12 and yClick <= 35:
        convertGrayscale(imgName, img, win)
    elif xClick >= 222 and xClick <= 304 and yClick >= 12 and yClick <= 35:
        convertNegative(imgName, img, win)
    elif xClick >= 18 and xClick <= 100 and yClick >= 12 and yClick <= 35:
        stats(img)
    
    # saves image and closes window if quit button is pressed
    elif xClick >= 324 and xClick <= 406 and yClick >= 12 and yClick <= 35:
        newImg = save()
        img.save(newImg + ".png")
        win.close()


# if "q" or "Q" is pressed, this function is called to save the image and then close the window
def handleKey(key, win):
    if key == "q" or key == "Q":
        newImg = save()
        img.save(newImg + ".png")
        win.close()


# main program that integrates other methods
def main():

    try:
        # get name of image file we need
        imgName = input("Enter the name of the image you want to open: ")
        # set loop to handle a blank input
        while imgName == "":
            imgName = input("Please enter the name of the image you want to open: ")

        # define image and window
        img, win = openImageAndWindow(imgName)

        # set loop that can get many clicks from user, and set values for x and y values
        while True:
            key = win.checkKey()
            click = win.checkMouse()

            # call handleClick function to respond to click
            if click != None:
                handleClick(click, imgName, img, win)
            if key != None:
                handleKey(key, win)

    except graphics.GraphicsError:
        print("Program exited.")


main()

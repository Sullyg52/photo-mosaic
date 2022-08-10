from http.client import NO_CONTENT
from PIL import Image
import math, glob

targetImg = Image.open('pictures/mom.jpg')
# Store source images
srcImgs = []
for file in glob.glob('pictures/sized-images/*'):
    srcImgs.append(Image.open(file))

WIDTH = srcImgs[0].width
HEIGHT = WIDTH
N_ROWS = 100
N_COLUMNS = targetImg.width // (targetImg.height // N_ROWS)

def main():
    # Get even square coords to be replaced and generate output image
    targetSquares = getSquares(targetImg)
    print(targetImg.size)
    print(targetSquares[len(targetSquares) - 1])
    print(targetImg.width // N_COLUMNS)

    # Create output image and generate square coords for it
    dim = (N_COLUMNS * WIDTH, N_ROWS * HEIGHT)
    newImg = Image.new('RGB', dim)
    outputSquares = getSquares(newImg)
    print(newImg.size)
    print(outputSquares[len(outputSquares) - 1])
    print(WIDTH)

    # Create list of average colors for each source image
    avgSrcColors = []
    for img in srcImgs:
        avgSrcColors.append(calcAvgColor(img))

    # Replace every square in new picture with best matching image from source images
    for sqIndex in range(len(targetSquares)):
        crop = targetImg.crop(targetSquares[sqIndex])
        matchingImg = srcImgs[findIndexClosestColor(crop, avgSrcColors)]
        newImg.paste(matchingImg, outputSquares[sqIndex])

    newImg.show()
    newImg.save('pictures/output.png')
        
# Divides up image into squares of the same size, and store the coords of each square into a list
def getSquares(img):
    # Get width and height of each square
    dWidth = img.width // N_COLUMNS
    dHeight = img.height // N_ROWS

    # Generate each square's coordinates
    squares = []
    for r in range(N_ROWS):
        for c in range(N_COLUMNS):
            x = c * dWidth
            y = r * dHeight
            squares.append((x, y, x + dWidth, y + dHeight))

    return squares

# Gets average color of a picture
def calcAvgColor(img):
    # Generate list of pixels in picture
    pixels = list(img.getdata())
    nPixels = len(pixels)

    r = 0
    g = 0
    b = 0
    # Add up r, g, and b values in every pixel
    for pixel in pixels:
        r += pixel[0]
        g += pixel[1]
        b += pixel[2]
    
    # Divide each by num of pixels to get avg and return
    return (r // nPixels, g // nPixels, b // nPixels)

# Get difference between 2 colors using distance formula
def calcDiffColor(colorA, colorB):
    totalSquareDiff = 0
    for a, b in zip(colorA, colorB):
        totalSquareDiff += (b - a) ** 2

    return math.sqrt(totalSquareDiff)

# Find index of color in list closest in color to inputted image
def findIndexClosestColor(img, colors):
    targetColor = calcAvgColor(img)

    # Find closest color by tracking the min difference in color found while looping through array
    closestColorIndex = 0
    min = calcDiffColor(targetColor, colors[0])
    for i in range(1, len(colors)): # Starts at 1 to skip 0 which is the preset
        diffColor = calcDiffColor(targetColor, colors[i])
        if diffColor < min:
            closestColorIndex = i
            min = diffColor

    return closestColorIndex

if __name__ == '__main__':
    main()
    targetImg.close()

    # Close all source images
    for img in srcImgs:
        img.close()
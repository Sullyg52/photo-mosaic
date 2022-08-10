from http.client import NO_CONTENT
from PIL import Image
import math, glob

SQUARE_WIDTH = 16

def main():
    # Get target image
    targetImg = Image.open('pictures/elk.png')
    # Get source images
    srcImgs = []
    for file in glob.glob('pictures/sized-images/*'):
        srcImgs.append(Image.open(file))

    # Get even square coords to be replaced
    targetSquares = getSquares(targetImg, SQUARE_WIDTH)
    print(targetImg.size)
    print(targetSquares[len(targetSquares) - 1])
    print(SQUARE_WIDTH)

    # Get source image width and use that to calculate dimensions of output image
    srcImagesWidth = srcImgs[0].width
    dim = ((targetImg.width // SQUARE_WIDTH) * srcImagesWidth, (targetImg.height // SQUARE_WIDTH) * srcImagesWidth)

    # Create output image
    outputImg = Image.new('RGB', dim)
    outputSquares = getSquares(outputImg, srcImagesWidth)
    print(outputImg.size)
    print(outputSquares[len(outputSquares) - 1])
    print(srcImagesWidth)

    # Create list of average colors for each source image
    avgSrcColors = []
    for img in srcImgs:
        avgSrcColors.append(calcAvgColor(img))

    # Replace every square in new picture with best matching image from source images
    for sqIndex in range(len(targetSquares)):
        crop = targetImg.crop(targetSquares[sqIndex])
        matchingImg = srcImgs[findIndexClosestColor(crop, avgSrcColors)]
        outputImg.paste(matchingImg, outputSquares[sqIndex])

    outputImg.show()
    outputImg.save('pictures/output.png')

    # Close all images
    targetImg.close()
    for img in srcImgs:
        img.close()
        
# Divides up image into squares of the same size, and store the coords of each square into a list
def getSquares(img, width):
    # Generate each square's coordinates
    squares = []
    y = width
    while y <= img.height:
        x = width
        while x <= img.width:
            squares.append((x - width, y - width, x, y))
            x += width

        y += width

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
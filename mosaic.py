from PIL import Image
import math, glob

WIDTH = 10

targetImg = Image.open('pictures/elk.png')

def main():
    # Get even square dimensions to be replaced and generate output image
    squares = getSquares()
    # Gets dimensions of new picture using WIDTH so there are no blank pixels
    dim = ((targetImg.width // WIDTH) * WIDTH, (targetImg.height // WIDTH) * WIDTH)
    newImg = Image.new('RGB', dim)

    # Store source images
    srcImgs = []
    for file in glob.glob('pictures/sized-images/*'):
        srcImgs.append(Image.open(file))

    # Create list of average colors for each source image
    avgSrcColors = []
    for img in srcImgs:
        avgSrcColors.append(calcAvgColor(img))

    # Replace every square in new picture with best matching image from source images
    for square in squares:
        crop = targetImg.crop(square)
        matchingImg = srcImgs[findIndexClosestColor(crop, avgSrcColors)]
        newImg.paste(matchingImg, square)

    newImg.show()

    # Close all source images
    for img in srcImgs:
        img.close()
        
# Divides up image into squares relatively the same size, and store the coords of each square into a list
def getSquares():
    # Generate each square's coordinates
    squares = []
    y = WIDTH
    while y <= targetImg.height:
        x = WIDTH
        while x <= targetImg.width:
            squares.append((x - WIDTH, y - WIDTH, x, y))
            x += WIDTH

        y += WIDTH

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
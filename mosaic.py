from http.client import NO_CONTENT
from PIL import Image, ImageOps
import math, glob

# Get target image
im = Image.open('pictures/elk.png')
im = ImageOps.exif_transpose(im) # Rotate if need be
targetImg = im.convert('RGB') # Convert to RGB img

N_ROWS = 144
SQUARE_WIDTH = targetImg.height // N_ROWS
N_COLUMNS = targetImg.width // SQUARE_WIDTH

def main():
    # Get source images
    srcImgs = []
    for file in glob.glob('pictures/sized-images/*'):
        srcImgs.append(Image.open(file))

    # Get even square coords to be replaced
    targetSquares = getSquares(targetImg, SQUARE_WIDTH)

    # Get source image width and use that to calculate dimensions of output image
    srcImagesWidth = srcImgs[0].width
    dim = (N_COLUMNS * srcImagesWidth, N_ROWS * srcImagesWidth)

    # Create output image
    outputImg = Image.new('RGB', dim)
    outputSquares = getSquares(outputImg, srcImagesWidth)

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
    outputImg.save('pictures/output.jpg')

    # Close all images
    targetImg.close()
    for img in srcImgs:
        img.close()
        
# Divides up image into squares of the same size, and store the coords of each square into a list
def getSquares(img, width):
    # Generate each square's coordinates
    squares = []
    for r in range(N_ROWS):
        h = r * width
        for c in range(N_COLUMNS):
            w = c * width
            squares.append((w, h, w + width, h + width))

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
from PIL import Image
import math, glob

WIDTH = 25
image = Image.open('pictures/lamelo.png')

def main():
    # Get even square dimensions to be replaced and generate output image
    squares = getSquares()
    newImg = Image.new('RGB', (image.width, image.height))

    # Open all cropped images
    # Get file names
    files = glob.glob('pictures/sized-images/*')
    # Store all image files in images list
    images = []
    for file in files:
        images.append(Image.open(file))

    # Replace every square in new picture with best matching image from source images
    for square in squares:
        crop = image.crop(square)
        matchingImg = findClosestImg(crop, images)
        newImg.paste(matchingImg, square)

    newImg.show()
        
# Divides up image into squares relatively the same size, and store the coords of each square into a list
def getSquares():
    # Generate each square's coordinates
    squares = []
    y = WIDTH
    while y <= image.height:
        x = WIDTH
        while x <= image.width:
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

# Find image in list closest in color to inputted image
def findClosestImg(target, images):
    # Get color we want to get closest to
    targetColor = calcAvgColor(target)

    # Find closest image in color by tracking the min distance in color found while looping through array
    closestImg = images[0]
    min = calcDiffColor(targetColor, calcAvgColor(images[0]))
    for img in images:
        diffColor = calcDiffColor(targetColor, calcAvgColor(img))
        if diffColor < min:
            closestImg = img
            min = diffColor

    return closestImg

if __name__ == '__main__':
    main()
    image.close()
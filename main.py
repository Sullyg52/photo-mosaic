from PIL import Image
import math

N_ROWS = 100
N_COLUMNS = N_ROWS
image = Image.open("lamelo.png")

def main():
    # Get even square dimensions to be replaced and generate output image
    squares = getSquares()
    newImg = Image.new("RGB", (image.width, image.height))

    # Replace every square in new picture with average color of the corresponding square in the original image
    for square in squares:
        imageCrop = image.crop(square)
        avgColor = getAvgColor(imageCrop)
        replaceSquare(newImg, square, avgColor)

    newImg.show()
        
# Divides up image into squares relatively the same size, and store the coords of each square into a list
def getSquares():
    # Get average width and height of each square
    dWidth = image.width / N_COLUMNS
    dHeight = image.height / N_ROWS

    # Generate each square coord
    squares = []
    for rows in range(N_ROWS):
        # Calc top and bottom coordinate, use ceiling to avoid a decimal and ensure every pixel is used
        top = math.ceil(rows * dHeight)
        bottom = math.ceil(top + dHeight)

        # Calc left and right coordinate
        for columns in range(N_COLUMNS):
            left = math.ceil(columns * dWidth)
            right = math.ceil(left + dWidth)

            squares.append((left, top, right, bottom))

    return squares

# Gets average color of a picture
def getAvgColor(img):
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

# Create new image of specified color and paste it into original image
def replaceSquare(img, square, color):
    width = square[2] - square[0]
    height = square[3] - square[1]
    newImg = Image.new("RGB", (width, height), color)

    img.paste(newImg, square)

main()
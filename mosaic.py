from PIL import Image, ImageOps
import math
import glob

# Get target image
im = Image.open('pictures/elk.png')
im = ImageOps.exif_transpose(im)  # Rotate if need be
target_img = im.convert('RGB')  # Convert to RGB im

n_rows = 144
square_width = target_img.height // n_rows
n_rows = target_img.height // square_width
n_columns = target_img.width // square_width


def main():
    # Get source images
    src_imgs = []
    for file in glob.glob('pictures/sized-images/*'):
        src_imgs.append(Image.open(file))

    # Get even square coords to be replaced
    target_squares = get_squares(target_img, square_width)

    # Get source image width and use that to
    # calculate dimensions of output image
    src_imgs_width = src_imgs[0].width
    dim = (n_columns * src_imgs_width, n_rows * src_imgs_width)

    # Create output image
    output_img = Image.new('RGB', dim)
    output_squares = get_squares(output_img, src_imgs_width)

    # Create list of average colors for each source image
    avg_src_colors = []
    for img in src_imgs:
        avg_src_colors.append(calc_avg_color(img))

    # Replace every square in new picture with best matching
    # image from source images
    for sq_index in range(len(target_squares)):
        crop = target_img.crop(target_squares[sq_index])
        matching_img = src_imgs[find_index_closest_color(crop, avg_src_colors)]
        output_img.paste(matching_img, output_squares[sq_index])

    output_img.show()
    output_img.save('pictures/output.jpg')

    # Close all source images
    for img in src_imgs:
        img.close()


# Divides up image into squares of the same size,
# and store the coords of each square into a list
def get_squares(img, width):
    # Generate each square's coordinates
    squares = []
    for r in range(n_rows):
        h = r * width
        for c in range(n_columns):
            w = c * width
            squares.append((w, h, w + width, h + width))

    return squares


# Gets average color of a picture
def calc_avg_color(img):
    # Generate list of pixels in picture
    pixels = list(img.getdata())
    n_pixels = len(pixels)

    r = 0
    g = 0
    b = 0
    # Add up r, g, and b values in every pixel
    for pixel in pixels:
        r += pixel[0]
        g += pixel[1]
        b += pixel[2]

    # Divide each by num of pixels to get avg and return
    return (r // n_pixels, g // n_pixels, b // n_pixels)


# Get difference between 2 colors using distance formula
def calc_diff_color(colorA, colorB):
    total_square_diff = 0
    for a, b in zip(colorA, colorB):
        total_square_diff += (b - a) ** 2

    return math.sqrt(total_square_diff)


# Find index of color in list closest in color to inputted image
def find_index_closest_color(img, colors):
    target_color = calc_avg_color(img)

    # Find closest color by tracking the min difference in
    # color found while looping through array
    closest_clr_index = 0
    min = calc_diff_color(target_color, colors[0])
    for i in range(1, len(colors)):  # Starts at 1 to skip default of 0
        diff_color = calc_diff_color(target_color, colors[i])
        if diff_color < min:
            closest_clr_index = i
            min = diff_color

    return closest_clr_index


if __name__ == '__main__':
    main()

from PIL import Image, ImageOps
import math
import glob

# Get target image
target_img = Image.open("pictures/elk.png")
target_img = ImageOps.exif_transpose(target_img)  # Rotate if need be
target_img = target_img.convert("RGB")  # Convert to RGB im

MIN_N_ROWS = 144

SQUARE_WIDTH = target_img.height // MIN_N_ROWS
N_ROWS = target_img.height // SQUARE_WIDTH
N_COLUMNS = target_img.width // SQUARE_WIDTH


def main():
    global target_img

    # Get source images
    src_imgs = []
    for file in glob.glob("pictures/sized-images/*"):
        src_imgs.append(Image.open(file))

    # Crop target image in the middle so that pixels lost will be evenly distributed
    target_img = crop_img_middle(
        target_img, (SQUARE_WIDTH * N_COLUMNS, SQUARE_WIDTH * N_ROWS)
    )

    # Get even square coords to be replaced
    target_squares = get_squares(target_img, SQUARE_WIDTH)
    print(target_img.size)
    print(target_squares[0])
    print(target_squares[len(target_squares) - 1])
    print(SQUARE_WIDTH)

    # Get source image width and use that to
    # calculate dimensions of output image
    src_imgs_width = src_imgs[0].width
    dim = (N_COLUMNS * src_imgs_width, N_ROWS * src_imgs_width)

    # Create output image
    output_img = Image.new("RGB", dim)
    output_squares = get_squares(output_img, src_imgs_width)
    print(output_img.size)
    print(output_squares[len(output_squares) - 1])
    print(src_imgs_width)

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
    output_img.save("pictures/output.jpg")

    # Close all source images
    for img in src_imgs:
        img.close()


# Divides up image into squares of the same size,
# and store the coords of each square into a list
def get_squares(img, width):
    # Generate each square's coordinates
    squares = []
    for r in range(N_ROWS):
        h = r * width
        for c in range(N_COLUMNS):
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


def crop_img_middle(img, size):
    """Downsizes image to given size by cropping the image an even amount on all sides

    Args:
        img (Image): Image to be cropped
        size (tuple[int, int]): Width, height to crop image to

    Returns:
        Image: Cropped image
    """
    dim = (
        (img.width - size[0]) // 2,
        (img.height - size[1]) // 2,
        (img.width + size[0]) // 2,
        (img.height + size[1]) // 2,
    )

    return img.crop(dim)


if __name__ == "__main__":
    main()

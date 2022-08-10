import glob
from PIL import Image, ImageOps

WIDTH = 128
HEIGHT = WIDTH

def main():
    # Get file names
    files = glob.glob('pictures/source-images/*')

    # Store all image files in images list
    images = []
    for file in files:
        im = Image.open(file)
        im = ImageOps.exif_transpose(im) # Rotate if need be
        images.append(im.convert('RGB')) # Convert to RGB img

    # Crop all images and save them
    for i in range(len(images)):
        cropped = images[i].resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        images[i].close()
        cropped.save(f'pictures/sized-images/image{i + 1}.jpg')



if __name__ == '__main__':
    main()
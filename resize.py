import glob
from PIL import Image

WIDTH = 50
HEIGHT = WIDTH

def main():
    # Get file names
    files = glob.glob('pictures/source-images/*')

    # Store all image files in images list
    images = []
    for file in files:
        images.append(Image.open(file))

    # Crop all images and save them
    for i in range(len(images)):
        cropped = images[i].resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        images[i].close()
        cropped.save(f'pictures/cropped-images/image{i + 1}.{images[i].format.lower()}')



if __name__ == '__main__':
    main()
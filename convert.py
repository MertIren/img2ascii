import argparse
from PIL import Image
import os
from termcolor import cprint

def convertToText(image_path, output_path, scale, color):
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_path)

    if output_path is not None:
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
        if color:
            print("Can't use color outside of terminal")
        color = False

    im = Image.open(image_path)
    pixels = im.getdata()
    width, height = im.size

    pixels = list(pixels)
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    if output_path is not None:
        f = open(output_path, "w")
    else: f = None

    for i in range(0, len(pixels), scale*2):
        row = pixels[i]
        for j in range(0, len(row), scale):
            pixel = row[j]

            if not color:
                avg = sum(pixel)/3
                if avg <= 25:
                    char = "."
                elif avg <= 75:
                    char = ","
                elif avg <= 125:
                    char = "*"
                elif avg <= 175:
                    char = "%"
                else:
                    char = "#"
                
                if f:
                    f.write(char)
                else:
                    print(char, end="")
            else:
                cprint("#", pixel, end="")
        if f:
            f.write("\n")
        else:
            print("")
    if f:
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="img2ascii",
        description="Converts an image into ASCII text"
    )
    parser.add_argument("-i", "--image", required=True)
    parser.add_argument("-o", "--output")
    parser.add_argument("-s", "--scale", default=1, type=int)
    parser.add_argument("-c", "--color", default=False)
    args = parser.parse_args()

    convertToText(args.image, args.output, args.scale, args.color)
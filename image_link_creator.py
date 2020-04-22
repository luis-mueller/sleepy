
import os
import sys

path = sys.argv[1]
link = sys.argv[2]

images = os.listdir(path)

for image in images:

    imageName = image.split(".")[0]

    print("[{}]: {}/{}".format(
        imageName,
        link,
        image.lower()
    ))

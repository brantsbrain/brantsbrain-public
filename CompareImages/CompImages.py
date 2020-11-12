# Compare two pictures at a time from a given directory to see if they match. Option to delete or just state matching images.
# Used code from https://rosettacode.org/wiki/Percentage_difference_between_images#Python to accomplish this
from PIL import Image
from tkinter import filedialog
import os, keyboard, hashlib

# Import string paths and return int for similarity. 0 means the images were exactly equal
def compImages(image1path, image2path):
    i1 = Image.open(image1path)
    i2 = Image.open(image2path)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents

# Compare hashes instead of pixels
def compHashes(image1path, image2path):
    with open(image1path, "rb") as reader:
        file1hash = hashlib.md5(reader.read().encode()).hexdigest()
    with open(image2path, "rb") as reader:
        file2hash = hashlib.md5(reader.read().encode()).hexdigest()

    if file1hash == file2hash:
        return 0
    else:
        return 1

# Select directory and confidence
directory = filedialog.askdirectory()
confidence = input("Enter confidence [0]: ")

if confidence == "":
    confidence = 0
else:
    confidence = int(confidence)

print("Press the N key during runtime to print which index the program is working on")
listdir = os.listdir(directory)
print("Total images: " + str(len(listdir)))

# Begin loop at index 0 of listdir
for file1num in range(len(listdir) - 1):
    filename1 = directory + "/" + os.fsdecode(listdir[file1num])

    # Begin loop at current index of outer loop to avoid comparing files twice
    for file2num in range(file1num + 1, len(listdir)):
        filename2 = directory + "/" + os.fsdecode(listdir[file2num])

        # Check to see which index the outer loop is on if the N key is pressed
        if keyboard.is_pressed("n"):
            print(str(file1num), end="\r")

        # Only run the compImages() method if the two files share the same file extensions
        if (filename1.endswith(".jpeg") and filename2.endswith(".jpeg")) or (filename1.endswith(".png") and filename2.endswith(".png")):
            try:
                if compHashes(filename1, filename2) == 0:
                    print("Found matching images: " + filename1 + " and " + filename2 + "\n\n")
                # if compImages(filename1, filename2) == confidence:
                #     print("Found matching images: " + filename1 + " and " + filename2 + "\n\n")
                    # Insert optional delete logic
            except Exception as e:
                # print("An error occurred with " + filename1 + " and " + filename2 + ": " + str(e) + "\n\n")
                pass

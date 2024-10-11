from  multiprocessing import pool
import cv2
import numpy as np
import math
import random
import argparse
from os import listdir

# Argument Parsing
argParser = argparse.ArgumentParser(prog='Dumb Face Swirling App',
                                    description='A dumb app that detects faces in an image and swirls them. Works with anime faces too.')

# argParser.add_argument('filename')
argParser.add_argument('-v', '--verbose', action='store_true', help='Used for debugging purposes.')
argParser.add_argument('-a', '--anime', action='store_true', help='Uses anime face detection instead of regular face detection.')
argParser.add_argument('-r', '--radius', default=2, type=float, help='Increases the radius of the swirl around the face by a multiplier.')
argParser.add_argument('-y', '--yadjust', default=-0.1, type=float, help='Vertically adjusts the swirl up or down by a percentage of the size based on a positive/negative number respectively.')
argParser.add_argument('-t', '--tension', default=0.75, type=float, help='Adjusts the swirl\'s strength and how fast it reaches the max value.')
argParser.add_argument('-cw', '--clockwise', action='store_true', help='Makes all swirls clockwise.')
argParser.add_argument('-ccw', '--counterclockwise', action='store_true', help='Makes all swirls counterclockwise.')
argParser.add_argument('-min', '--minangle', default=150, type=float, help='Sets the minimum range of the swirl angle.')
argParser.add_argument('-max', '--maxangle', default=420, type=float, help='Sets the maximum range of the swirl angle.')
argParser.add_argument('-f', '--file', help='Target a single file instead of the entire directory. Useful if you have a lot of images in the working directory')
args = argParser.parse_args()

args.verbose and args.anime and print('--anime flag enabled. Detecting anime faces instead.')

pool = pool.ThreadPool()

direction = [-1,1]
if args.clockwise and args.counterclockwise:
    print('Invalid flags: Both -cw and -ccw detected. Pick only -cw or -ccw or neither.')
    exit()
if args.clockwise:
    direction = [-1]
if args.counterclockwise:
    direction = [1]

# Helper functions
def isImage(fileName):
    return str.endswith(fileName, ('png', 'jpg', 'jpeg', 'bmp', 'tiff','jfif'))

def isSwirled(fileName):
    return str.startswith(fileName, 'swirled_')

def getValidFiles():
    return filter(lambda x: not isSwirled(x) and isImage(x), listdir('.'))

# Swirling functions
def swirl_effect(image, center, radius, angle, tension):
    height, width = image.shape[:2]
    output = np.zeros_like(image)

    for y in range(height):
        for x in range(width):
            dx = x - center[0]
            dy = y - center[1]
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < radius:
                percentage = math.pow(distance / radius, math.pow(1- distance/radius, tension))
                swirl_amount = 1 - percentage
                theta = swirl_amount * math.radians(angle)
                xs = int(center[0] + math.cos(theta) * dx - math.sin(theta) * dy)
                ys = int(center[1] + math.sin(theta) * dx + math.cos(theta) * dy)
                output[y, x] = image[min(height-1, max(0, ys)), min(width-1, max(0, xs))]
            else:
                output[y, x] = image[y, x]
    return output

def swirlFaces(imagePath):
    if(args.anime):
        face_cascade = cv2.CascadeClassifier('./lbpcascade_animeface.xml')
    else:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # Expanding the rectangle to include more of the head
            new_w = int(w * args.radius)
            new_h = int(h * args.radius)
            new_x = x - (new_w - w) // 2
            new_y = y - (new_h - h) // 2 - int(h * args.yadjust)

            # Ensuring the new coordinates are within the image boundaries
            new_x, new_y = max(0, new_x), max(0, new_y)
            new_w, new_h = min(image.shape[1] - new_x, new_w), min(image.shape[0] - new_y, new_h)

            face_img = image[new_y:new_y+new_h, new_x:new_x+new_w]
            swirled_face = swirl_effect(face_img, (new_w//2, new_h//2), min(new_w//2, new_h//2), random.choice(direction) * random.randrange(args.minangle,args.maxangle), args.tension)  # Angle set to 270 degrees
            image[new_y:new_y+new_h, new_x:new_x+new_w] = swirled_face

        cv2.imwrite('swirled_' + imagePath, image)
        print("Swirled all faces and saved to " + 'swirled_' + imagePath)
    else:
        print("No faces to swirl, skipping.")

# Main flow
if args.file:
    if isImage(args.file):
        swirlFaces(args.file)
    else:
        print('Error: File is not an image.')
else:
    images = getValidFiles()
    tasks = []
    for img in images:
        tasks.append([img])

    if(args.verbose):
        for e in images:
            print(e)

    result = pool.starmap_async(swirlFaces,tasks)
    result.wait()

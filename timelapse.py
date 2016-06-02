#!/usr/bin/python
# coding=UTF-8
comm='''
    AUTHOR: ThomasWe
    DESCRIPTION: Python Script to generate a time lapse movie from images.
    Image File Name Pattern: yyyy-mm-dd-HH-MM.jpg
'''
import sys
import io
import time
import glob
import os
from datetime import datetime

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#CONFIG
FIRSTDAY = "30/5/2016"
FRAMERATE = 10
FONTSIZE = 60
ROTATE = True
DEGREE = 180

date_format = "%d/%m/%Y"

#check arguments
try:
   path = sys.argv[1]
except IndexError:
   print "ERROR: give a path to the image directory"
   sys.exit()

#exit if path does not exists
if not os.path.exists(path):
   print "ERROR: given path does not exists"
   sys.exit()

#start date (the day of the first image)
startingdate = datetime.strptime(FIRSTDAY, date_format)

#load pictures from folder
filelist =  glob.glob(path + "/*.jpg")
count = len(filelist)

#create folder movie
if not os.path.exists(path + "/movie"):
    os.makedirs(path + "/movie")

for i in xrange(count):
   # load picture
   img = Image.open(filelist[i])
   #calculate date difference
   filename = os.path.basename(filelist[i])
   imgdatearray = filename.split("-")
   delta = datetime.strptime(imgdatearray[2]+"/"+imgdatearray[1]+"/"+imgdatearray[0],date_format) - startingdate
   
   # rotate picture (180°)
   if ROTATE:
      img = img.rotate(DEGREE)
   
   # write day count to the left upper corner
   draw = ImageDraw.Draw(img)
   font = ImageFont.truetype("Arial.ttf", FONTSIZE)
   draw.text((10, 10),"Tag " + str(delta.days + 1),(255,255,255),font=font)
   
   # save new image
   img.save(path + "/movie/img" + str(i) + ".jpg")

print os.popen("./ffmpeg -framerate "+ str(FRAMERATE) +" -start_number 0 -i " + path.replace(" ", "\ ") +"/movie/img%d.jpg -f mp4 -vcodec h264 "+ path.replace(" ", "\ ") +"/movie/film.mp4").read()

print os.popen("rm "+ path.replace(" ", "\ ") + "/movie/img*").read()
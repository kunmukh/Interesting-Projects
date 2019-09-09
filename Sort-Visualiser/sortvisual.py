#!/usr/bin/python3

import sys
import time
import numpy as np
from tkinter import *
from PIL import Image, ImageTk


class MainWindow():

    def __init__(self, main, image, my_images):

        # canvas for image
        self.canvas = Canvas(main, width=image.width(), height=image.height())
        self.canvas.grid(row=0, column=0)

        # images
        self.my_images = my_images
        self.my_image_number = 0

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0,0, anchor = NW, image = image)

        self.button = Button(main, text="Next Pic", command=self.onButton)
        self.button.grid(row=image.width()+10, column=image.height()+10)

    def runImageFilm(self):

        # next image
        self.my_image_number += 1

        # return to first image
        if self.my_image_number == len(self.my_images):
            self.my_image_number = 0

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])

    def onButton(self):
    	self.runImageFilm()

    def onButton_click(self):
    	self.button.invoke()

class ImageStorage():

	my_images = []

	def __init__(self, image):
		self.image = image
		self.my_images.append(image)

	def add_image(self, image):
		self.my_images.append(image)
		# print(self.my_images)

	def get_images(self):
		return self.my_images


def createImagefromArr(arr, imageArr):

	arrTemp = imageArr

	for i in range(len(arr)):
		arrTemp[i] = imageArr[arr[i]]

	return ImageTk.PhotoImage(Image.fromarray(arrTemp))

def main():

	try:
		tatras = Image.open("example.jpg")

	except IOError:
		("Unable to load image")
		sys.exit(1)

	root = Tk()
	imgArr = ImageStorage(ImageTk.PhotoImage(tatras))

	A = np.array(tatras)
	A.setflags(write=1)

	sortA = np.arange(len(A))
	np.random.shuffle(sortA)	

	# Traverse through all array elements 
	for i in range(len(sortA)): 
	      
	    # Find the minimum element in remaining  
	    # unsorted array 
	    min_idx = i 
	    for j in range(i+1, len(sortA)): 
	        if sortA[min_idx] > sortA[j]: 
	            min_idx = j 
	              
	    # Swap the found minimum element with  
	    # the first element         
	    sortA[i], sortA[min_idx] = sortA[min_idx], sortA[i]	    
	    
	    imgArr.add_image(createImagefromArr(sortA, A))	    	
	    # print(i)

	# Driver code to test above 
	print ("Sorted array") 
	# for i in range(len(sortA)): 
	#     print("%d" %sortA[i]),
	
	m = MainWindow(root, ImageTk.PhotoImage(tatras), imgArr.get_images())
	while True:
		m.onButton_click() 
		time.sleep(2)
		root.update()



if __name__ == '__main__':
    main()


#!/usr/bin/python3

# Kunal Mukherjee
# Slection Sort Visualizer
# 9/9/19

#import library
import sys
import time
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# MainWindow is the class that provide the canvas
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

        # set button for an image
        self.button = Button(main, text="Next Picture", command=self.onButton)
        self.button.grid(row=image.width() + 30, column=image.height())

        self.button1 = Button(main, text="Restart", command=self.restartButton)
        self.button1.grid(row=image.width() - 30, column=image.height())

    def runImageFilm(self):

        # next image
        self.my_image_number += 1

        # return to first image
        if self.my_image_number == len(self.my_images):
            self.my_image_number = len(self.my_images) - 1

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])

    def onButton(self):
		# Start the filmmade ofimages
    	self.runImageFilm()

    def onButton_click(self):
    	# Method to invoke the button in software
    	self.button.invoke()

    def restartButton(self):
    	# check to see if end of frame then restart
    	if self.my_image_number == (len(self.my_images) - 1):
            self.my_image_number = 0

#  Class to store the umsorted images
class ImageStorage():

	# list if temporary images
	my_images = []

	def add_image(self, image):
		self.my_images.append(image)
		# print(self.my_images)

	def get_images(self):
		return self.my_images

# Creates am image from array
def createImagefromArr(arr, imageArr):

	arrTemp = imageArr.copy()

	for i in range(len(arr)):
		arrTemp[i] = imageArr[arr[i]]

	return ImageTk.PhotoImage(Image.fromarray(arrTemp))

# Selection Sort
def selectionSort(indexImgArr, imgStoragearr, originalImgarr):
	
	sortImgindexArr = []

	# Traverse through all array elements 
	for i in range(len(indexImgArr)): 
	      
	    # Find the minimum element in remaining  
	    # unsorted array 
	    min_idx = i 
	    for j in range(i+1, len(indexImgArr)): 
	        if indexImgArr[min_idx] > indexImgArr[j]: 
	            min_idx = j 
	              
	    # Swap the found minimum element with  
	    # the first element         
	    indexImgArr[i], indexImgArr[min_idx] = indexImgArr[min_idx], indexImgArr[i]	    
	    
	    sortImgindexArr.append(indexImgArr.copy())

	return sortImgindexArr  

def flipArray(A):
	tempA = A.copy()

	for i in range(len(A)):
		tempA[i] = A[len(A) - i - 1]

	return tempA  

# the main driver program
def main():

	# try to open an image
	try:
		tatras = Image.open(sys.argv[1])

	except IOError:
		("Unable to load image")
		sys.exit(1)

	# intitilaze the Tkinter object
	root = Tk()
	root.title("Selection Sort Visualizer -- Kunal Mukherjee")

	# creating an instance of ImageStorage
	imgArr = ImageStorage()

	# creating an array ofthe image
	A = np.array(tatras)	

	# creating an image from the original array
	# display the image
	img = Image.fromarray(A)
	img.show()

	# array of the index of the image array
	indexA = np.arange(len(A))
	# shuffle the image 
	np.random.shuffle(indexA)	

	# Selection Sort Algorithm
	sortImgArr = selectionSort(indexA, imgArr, A)	

	# Store the image created from the temporary sorted image array
	for i in range(len(sortImgArr)):
		imgArr.add_image(createImagefromArr(sortImgArr[i], A))

	# Debugging message
	print ("Sorted array")
	
	# intitilize the main window
	m = MainWindow(root, ImageTk.PhotoImage(tatras), imgArr.get_images())

	while True:
		#create a button click event every .2 sec
		m.onButton_click() 
		time.sleep(.05)
		root.update()


if __name__ == '__main__':
    main()


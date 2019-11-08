#!/usr/bin/python3

# Kunal Mukherjee
# Image Flipper
# 9/9/19

#import library
import sys
import time
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 

def test(A):
	tempA = A.copy()

	for i in range(len(A)):
		tempA[i] = A[len(A) - i - 1]

	return tempA
	
# the main driver program
def main():
	tatras = Image.open(sys.argv[1])
	# creating an array ofthe image
	A = np.array(tatras)

	A = test(A)

	# creating an image from the original array
	# display the image
	img = Image.fromarray(A)
	img.show()

	


if __name__ == '__main__':
    main()


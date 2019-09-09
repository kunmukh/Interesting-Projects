#!/usr/bin/python3

from PIL import Image, ImageTk
import sys
import time
import numpy as np

def imageShow(arr, imageArr):

	#global img

	arrTemp = imageArr

	for i in range(len(arr)):
		arrTemp[i] = imageArr[arr[i]]

	img = Image.fromarray(arrTemp)
	img.show()

try:
    tatras = Image.open("example.jpg")

except IOError:
    print("Unable to load image")
    sys.exit(1)
    
#cropped = tatras.crop((100, 100, 350, 350))
#cropped.show()
#print("Format: {0}\nSize: {1}\nMode: {2}".format(tatras.format, 
#    tatras.size, tatras.mode))
#cropped.save('tatras_cropped.jpg')
#size_picture = tatras.size

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
    
    if (i % 40 == 0) :
    	imageShow(sortA, A)
    	time.sleep(.002)
    

imageShow(sortA, A)

# Driver code to test above 
print ("Sorted array") 
for i in range(len(sortA)): 
    print("%d" %sortA[i]),


import cv2
import numpy as np
import glob

def sort_contours(cnts, method):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def getIntermediate(source, dest, kernel1, kernel2):
    filenames = glob.glob("image_processing/intermediate/" + source +  "/*.png")
    # filenames.sort()
    for img in filenames:
        print(img)
        image = cv2.imread('image_processing/intermediate/' + source + '/roi0.png')
        # image = cv2.resize(image,None,fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
        getContours(image,kernel1,kernel2, dest, 'left-to-right')
        # cv2.imshow('image',image)
        # cv2.waitKey(0)


def getContours(image, kernel1, kernel2, path, ctr_ordering):
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray',gray)
    # cv2.waitKey(0)
    #binary
    ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow('second',thresh)
    cv2.waitKey(0)

    #dilation
    kernel = np.ones((kernel1,kernel2), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    # cv2.imshow('dilated',img_dilation)
    cv2.waitKey(0)

    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort contours
    sorted_ctrs = sort_contours(ctrs,ctr_ordering);

    i = 0

    for ctr in ctrs:
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        # show ROI
        # cv2.imshow('segment no:'+str(i),roi)
        cv2.imwrite('image_processing/intermediate/' + path + '/roi' +str(i) +'.png',roi)
        i+=1
        # cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
        # cv2.waitKey(0)


#import image
image = cv2.imread('image_processing/test_images/CVL/0001-1-cropped.tif')
image = cv2.resize(image, (1000,700 ))
img_copy = image.copy()  
getContours(img_copy, 5, 100,'lines','top-to-bottom')
getIntermediate('lines', 'words', 5, 15)
getIntermediate('words', 'chars', 5, 5)
# cv2.imshow('orig',img_copy)
# cv2.waitKey(0)


# cv2.imshow('marked areas',image)
# cv2.waitKey(0)
# openImages()


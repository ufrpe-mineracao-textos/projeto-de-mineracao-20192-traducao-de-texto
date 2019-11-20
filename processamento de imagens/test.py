import cv2
import numpy as np
import glob
import pytesseract

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
	return (cnts, boundingBoxes)

def draw_contour_order(image, c, i):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
 
	# draw the countour number on the image
	cv2.putText(image, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (255, 0, 0), 2)
 
	# return the image with the contour number drawn on it
	return image

def getLinesFromImage(image, kernel1, kernel2, ctr_ordering):
    lines = []
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #binary
    ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow('gray', thresh)
    # cv2.waitKey(0)

    #dilation
    kernel = np.ones((kernel1,kernel2), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    # cv2.imshow('dilated',img_dilation)
    # cv2.waitKey(0)

    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    #sort contours
    sorted_ctrs, boxes = sort_contours(ctrs,ctr_ordering);
    img_copy = image.copy()  
    for ctr in sorted_ctrs:
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]
        lines.append(roi)
        i+=1
        cv2.rectangle(img_copy,(x,y),( x + w, y + h ),(90,0,255),2)
        # draw_contour_order(img_copy, ctr, i)
    cv2.imshow('orig',img_copy)
    cv2.waitKey(0)
    return lines

def getWordsFromLine(image, kernel1, kernel2, ctr_ordering):
    words = []
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #binary
    ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
    
    # cv2.waitKey(0)

    #dilation
    kernel = np.ones((kernel1,kernel2), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    # cv2.imshow('dilated',img_dilation)
    # cv2.waitKey(0)

    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort contours
    sorted_ctrs, boxes = sort_contours(ctrs,ctr_ordering);

    i = 0

    for ctr in sorted_ctrs:
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]
        # resized = cv2.resize(roi, (100,50))
        words.append(roi)
        i+=1
        cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
        # draw_contour_order(image, ctr, i)
    return words
    
#import image
image = cv2.imread('image_processing/test_images/IAM/a01-003.png')
# image = cv2.resize(image, (1333,300))
image = cv2.resize(image,(720,1240))
img_copy = image.copy()  
cv2.imshow('image', img_copy)
cv2.waitKey(0)
lines = getLinesFromImage(img_copy, 2, 50,'top-to-bottom')
print("Showing Lines")
for line in lines:
    # cv2.imshow('line', line)
    # cv2.waitKey(0)
    # print(pytesseract.image_to_string(line))
    words = getWordsFromLine(line, 3, 15,'left-to-right')
    for word in words:
        print(pytesseract.image_to_string(word))
        # cv2.imshow('word',word)
        # cv2.waitKey(0)


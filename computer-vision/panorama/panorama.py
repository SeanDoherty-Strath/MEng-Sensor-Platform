### Imports ###
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np

### Show Images ####
def showImage(image, title='Snapshot'):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

### Convert to Cylindrical Projection ####
def cylindricalProjection(img):

    # Simplified intrinsic matrix
    h, w = img.shape[:2]
    K = np.array([[w/2, 0, w/2],[0, w/2, h/2],[0, 0, 1]])  
    map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
    
    theta = (map_x - w / 2) / (w / 2)
    phi = (map_y - h / 2) / (h / 2)
    
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(phi)
    z = np.cos(theta) * np.cos(phi)
    
    map_x = (w / 2) * (x / z + 1)
    map_y = (h / 2) * (y / z + 1)

    cylindricalProjection = cv2.remap(img, map_x.astype(np.float32), map_y.astype(np.float32), cv2.INTER_LINEAR)

    # Crop to Smallest Rectangle
    gray = cv2.cvtColor(cylindricalProjection, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest_contour)
        
    cylindricalProjection = cylindricalProjection[y:y+h, x:x+w]
        
    return cylindricalProjection


### Take Two Images, Return Homography Matrix ####
def calculateHomography(referenceImage, warpImage):

    # Perform SIFT
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(referenceImage, None)
    kp2, des2 = sift.detectAndCompute(warpImage, None)

    # Match Features
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    
    # Find Good matches
    goodMatches = []
    threshold = 0.75
    for m, n in matches:
        if m.distance < threshold * n.distance:
            goodMatches.append(m)

    # Show Images
    if (False):
        # Show Features
        frame1withKeypoints = cv2.drawKeypoints(warpImage, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        showImage(frame1withKeypoints, 'Frame 1')
        frame2withKeypoints = cv2.drawKeypoints(referenceImage, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        showImage(frame2withKeypoints, 'Frame 2')

        # Show Descriptors
        sampleDescriptors = des1[:1]
        for i, descriptor in enumerate(sampleDescriptors, start=1):
            plt.plot(descriptor, label=f"Descriptor {i}")
        plt.show()

        # Show Matches
        matchedImage = cv2.drawMatchesKnn(referenceImage, kp1, warpImage, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        showImage(matchedImage)
        goodMatchesImage = cv2.drawMatches(referenceImage, kp1, warpImage, kp2, goodMatches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS, matchesThickness=1)
        showImage(goodMatchesImage)

    if len(goodMatches) > 4: # Ensure there are  enough matches for homography 

        src_pts = np.float32([kp1[m.queryIdx].pt for m in goodMatches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in goodMatches]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        return H
    else:
        print("Not enough matches found to compute homography.")

### Apply Homography ###
def applyHomography(referenceImage, warpImage, H):

    result = cv2.warpPerspective(warpImage, H, (referenceImage.shape[1] + warpImage.shape[1], referenceImage.shape[0]))
    result[0:referenceImage.shape[0], 0:referenceImage.shape[1]] = referenceImage

    return result

### Dewarp Image ####
def dewarpImage(image):
    height, width = image.shape[:2]
    for x in range(width):
        for y in range(height):
            pixel = list(image[y, x])
            
            # Find first non black pixel
            if pixel != [0, 0, 0]:
                image[y:y+5, x] = [0, 255, 0]
                start = y
                break  

        for y in range(height-1, 0, -1):
            pixel = list(image[y, x])
            
            # Find last non black pixel
            if pixel != [0, 0, 0]:
                image[y:y+5, x] = [0, 255, 0]
                end = y
                break  # Move to the next column after marking the first non-black pixel
        
        # Strect pixels
        sourcePixels = image[start:end, x, :]
            
        # Stretch the extracted range to the target height
        stretchedPixels = cv2.resize(sourcePixels[:, np.newaxis],(1, height), interpolation=cv2.INTER_LINEAR).squeeze()  # Remove the singleton dimension
            
        # Assign stretched pixels to the new image
        image[:, x, :] = stretchedPixels

    return image

### Main Function - this will be called from UI ####
def getPanorama(leftImage, rightImage):
    showImage(leftImage, 'Left Image')
    showImage(rightImage, 'Right Image')

    leftImage = cylindricalProjection(leftImage)
    rightImage = cylindricalProjection(rightImage)


    H = calculateHomography(leftImage, rightImage)
    panorama = applyHomography(leftImage, rightImage, H)
    showImage(panorama)

    panoramaDewarped = dewarpImage(panorama)
    showImage(panoramaDewarped)



### Testing ###
leftImage = cv2.imread('./computer-vision/panorama/IMG_2588.JPG')
rightImage = cv2.imread('./computer-vision/panorama/IMG_2589.JPG')
getPanorama(leftImage, rightImage) 

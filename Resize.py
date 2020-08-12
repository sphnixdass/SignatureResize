#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_brief/py_brief.html#brief
#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html#sift-intro
#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_orb/py_orb.html#orb

import cv2
import numpy as np
import os

tempfolderpath = '/data/Backup/Coding/Python/CV/SignatureResize'

def cropfunction(tempfoldername, tempfilename, tempinpputfile):
    im_gray = cv2.imread(tempinpputfile, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh = 50
    #thresh = 127
    bestthresh = 0
    tempthresh = 0
    threshstart = 100
    threshbreak = 25
    for i in range(threshstart,250,5):
        bestthresh = i
        im_bw = cv2.threshold(im_gray, i, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(str(len(contours)) + " --> " + str(i))
        #print((len(contours) - tempthresh)/len(contours))
        if (len(contours) - tempthresh) > threshbreak and i != threshstart:
            bestthresh = bestthresh -5
            break
        tempthresh =  len(contours)

    im_bw = cv2.threshold(im_gray, bestthresh, 255, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(im_bw.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    tempx = 0
    tempy = 0
    tempw = 0
    temph = 0
    tempwh =0 

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        print(x,y,w,h, w*h)
        if x > 20 and y > 20 and w >50 and h> 50:
            if (w*h) > tempwh:
                tempx = x
                tempy = y
                tempw = w
                temph = h
                tempwh = w*h

    print("final " + str(tempw * temph))
    print(im_bw)

    tempx2 = tempx
    tempy2 = tempy
    tempw2 = tempw
    temph2 = temph


    rowcount, colcount = im_bw.shape
    im_bw[im_bw > 100] = 255
    im_bw[im_bw < 100] = 0

    tempcalbreakvalue = 10
    tempmaxlifetickness = 15


    #extending right
    tempcal =0
    tempcalempty = 0
    tempcal2 =0
    tempcalflag = False
    for k in range(tempx + tempw,colcount):
        tempcal = np.count_nonzero(im_bw[tempy:tempy + temph,tempx + tempw:k] != 255)
        tempcalempty = tempcalempty + 1
        if (tempcal2 - tempcal) != 0 and (tempcal - tempcal2)  < tempmaxlifetickness:
            tempcalempty = 0
            tempcalflag = True
        tempcal2 = tempcal
        #cv2.imwrite('Test2.png', im_bw[tempy:tempy + temph,tempx + tempw:k + 1])
        if tempcalempty > tempcalbreakvalue and tempcalflag == True:
            tempw = (k - tempx) 
            break
        elif tempcalempty > tempcalbreakvalue and tempcalflag == False:
            break
        
    #extending left
    tempcal =0
    tempcalempty = 0
    tempcal2 =0
    tempcalflag = False
    #im_bw[tempy:tempy + temph,:tempx] = 1
    for k in range(tempx, 1, -1):
        tempcal = np.count_nonzero(im_bw[tempy:tempy + temph,k:tempx] != 255)
        tempcalempty = tempcalempty + 1
        if (tempcal2 - tempcal) != 0 and (tempcal - tempcal2)  < tempmaxlifetickness:
            tempcalempty = 0
            tempcalflag = True
        tempcal2 = tempcal
        #cv2.imwrite('Test2.png', im_bw[tempy:tempy + temph,k - 1:tempx])
        if tempcalempty > tempcalbreakvalue and tempcalflag == True:
            tempx = k
            break
        elif tempcalempty > tempcalbreakvalue and tempcalflag == False:
            break

    #extending bottom
    tempcal =0
    tempcalempty = 0
    tempcal2 =0
    tempcalflag = False
    #im_bw[tempy + temph:,tempx:tempx + tempw+1] = 1
    for k in range(tempy + temph, rowcount):
        tempcal = np.count_nonzero(im_bw[tempy + temph:k,tempx:tempx + tempw] != 255)
        tempcalempty = tempcalempty + 1
        if (tempcal2 - tempcal) != 0 and (tempcal - tempcal2)  < tempmaxlifetickness:
            tempcalempty = 0
            tempcalflag = True
        tempcal2 = tempcal

        if tempcalempty > tempcalbreakvalue and tempcalflag == True:
            temph = (k - tempy)
            break
        elif tempcalempty > tempcalbreakvalue and tempcalflag == False:
            break

    #extending top
    tempcal =0
    tempcalempty = 0
    tempcal2 =0
    tempcalflag = False
    #:tempy,tempx:tempx + tempw+1
    for k in range(tempy, 1, -1):
        tempcal = np.count_nonzero(im_bw[k:tempy,tempx:tempx + tempw] != 255)
        tempcalempty = tempcalempty + 1
        if (tempcal2 - tempcal) != 0 and (tempcal - tempcal2)  < tempmaxlifetickness:
            tempcalempty = 0
            tempcalflag = True
        tempcal2 = tempcal

        if tempcalempty > tempcalbreakvalue and tempcalflag == True:
            tempy = k
            break
        elif tempcalempty > tempcalbreakvalue and tempcalflag == False:
            break

        
    print(rowcount)
    print(im_bw[tempy:tempy + temph,tempx + tempw:tempx + tempw])
    im_bw[tempy:tempy + temph,tempx + tempw: colcount] = 1

    #rowstart
    #im_bw[tempy:tempy+1,:] = 1
    #row end
    #im_bw[tempy + temph:tempy + temph+1,:] = 1
    #colstart
    #im_bw[:,tempx:tempx+1] = 1
    #col end
    #im_bw[:,tempx + tempw:tempx + tempw+1] = 1

    #left
    #im_bw[tempy:tempy + temph,tempx + tempw:] = 1

    #right
    #im_bw[tempy:tempy + temph,:tempx] = 1

    #top
    #im_bw[:tempy,tempx:tempx + tempw+1] = 1

    #bottom
    #im_bw[tempy + temph:,tempx:tempx + tempw+1] = 1

    #find the tilt signature
    roi = im_bw[tempy:tempy+temph, tempx:tempx+tempw]
    rowcount, colcount = roi.shape
    topcount = np.count_nonzero(roi[:int(rowcount/2),:] != 255)
    print(topcount)
    topcountper = (topcount/(rowcount*colcount)/2)*100
    print(topcountper)
    bottomcount = np.count_nonzero(roi[int(rowcount/2):,:] != 255)
    bottomcountper = (bottomcount/(rowcount*colcount)/2)*100
    print(bottomcount)
    print(bottomcountper)

    img_rotate_90_clockwise = roi

    if (bottomcountper - topcountper) < 1 and ((colcount/(rowcount+colcount))*100) < 60:
        img_rotate_90_clockwise = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)


    print((colcount/(rowcount+colcount))*100)
    #tempcal = np.count_nonzero(roi[tempy + temph:k,tempx:tempx + tempw] != 255)
    cv2.imwrite(tempfoldername + "/" + tempfilename.lower().replace(".png","").replace("jpg","") + 'Output.png', img_rotate_90_clockwise)
    #break
    # cv2.imwrite(tempfoldername + "/" + 'Test.png', im_bw)

# cropfunction

# for x in os.walk('.'):

#     print (x)

for x in os.listdir(tempfolderpath):
    if os.path.isdir(x):
        # print (tempfolderpath + "/" + x)
        for x2 in os.listdir(tempfolderpath + "/" + x):
            if (".png" or ".jpg" in x2.lower()):
                if not ("Output.png".lower() in x2.lower()):
                    print(tempfolderpath + "/" + x + "/" + x2)
                    cropfunction(tempfolderpath + "/" + x, x2, tempfolderpath + "/" + x + "/" + x2)
                    
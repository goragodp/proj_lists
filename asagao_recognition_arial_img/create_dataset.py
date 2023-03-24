import cv2 as cv
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import math
#Image is too large, process with original size
#but display the smaller one
FILES_LABELS_IMG = sorted(glob('x_train/30m-1_labeled/*')) #get image with label mask
FILES_ORIG_IMG = sorted(glob('x_train/30m-1/*'))

def resizeWithAspectRatio(im, w=None, h=None, inter=cv.INTER_AREA):
    dim = None

    (origh,origw) = im.shape[:2]
    if w is None and h is None:
        raise "Error: please specify either width or heigth"
    elif w is None:
        r = h / float(origh)
        dim = (int(origw * r), h)
    elif h is None:
        r = w / float(origw)
        dim = (w, int(origh * r))

    return cv.resize(im, dim, interpolation=inter)


def get_label_data_from_highlight():
    
    i = 1

    for ori, label in zip(FILES_ORIG_IMG, FILES_LABELS_IMG):
        lower = np.array([0, 180, 250], dtype="uint8")
        upper = np.array([100, 255, 255], dtype="uint8")

        img_lab = cv.imread(label)
        img_ori = cv.imread(ori)

        mask = cv.inRange(img_lab, lower, upper)

        # # find  closed contour and fill
        cnt = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnt = cnt[0] if len(cnt) == 2 else cnt[1]

        for c in cnt:
            cv.drawContours(mask, [c], 0, (255, 255, 255), -1) # fill close area of contour

        crop = cv.bitwise_and(img_ori, img_ori, mask=mask)
       
        # plt.subplot(2, 2, 1), plt.imshow(resizeWithAspectRatio(img_ori, 800))
        # plt.subplot(2, 2, 3), plt.imshow(resizeWithAspectRatio(mask, 800))
        # plt.subplot(2, 2, 4), plt.imshow(resizeWithAspectRatio(crop, 800))
        # plt.subplot(2, 2, 2), plt.imshow(resizeWithAspectRatio(img_lab, 800))
        # plt.show()
        # cv.imshow('Original', resizeWithAspectRatio(img_ori, 800))
        # cv.imshow('Mask', resizeWithAspectRatio(mask, 800))
        # cv.imshow('Cropped', resizeWithAspectRatio(crop, 800))
        # cv.imshow('Highlight', resizeWithAspectRatio(img_lab, 800))
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        SAVE_FILE_NAME_X = "x_train_data_%d.png"
        SAVE_FILE_NAME_Y = "y_train_data_%d.png"

        for c in cnt:
            # draw a rectangle
            rect = cv.boundingRect(c)
            if rect[2] < 100 or rect[3] < 100: continue
            print(cv.contourArea(c))

            x,y,w,h = rect
            cv.rectangle(img_lab, (x,y), (x+w, y+h), (255,255,0), 20)
            ROI_IMG = img_ori[y:y + h, x: x + w,:]
            ROI_MASK = mask[y:y + h, x: x + w] 
            # plt.subplot(1,2,1), plt.imshow(ROI_IMG)
            # plt.subplot(1,2,2), plt.imshow(ROI_MASK)
            # plt.show()
            cv.imwrite(SAVE_FILE_NAME_Y % i, ROI_MASK)
            cv.imwrite(SAVE_FILE_NAME_X % i, ROI_IMG)
            i += 1

def test():
    #delete Yellow line in image
    lower = np.array([0, 180, 250], dtype="uint8")
    upper = np.array([100, 255, 255], dtype="uint8")
    
    img_lab = cv.imread('dataset/raw/DJI_20211208095108_0010_LABLED.jpg')
    img_ori = cv.imread('dataset/raw/DJI_20211208095108_0010.JPG')
    
    mask = cv.inRange(img_lab, lower, upper)

    # # find  closed contour and fill
    cnt = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnt = cnt[0] if len(cnt) == 2 else cnt[1]

    for c in cnt:
        cv.drawContours(mask, [c], 0, (255, 255, 255), -1) # fill close area of contour
        #draw a rectangle
        # rect = cv.boundingRect(c)
        # if rect[2] < 100 or rect[3] < 100: continue
        # print(cv.contourArea(c))

        # x,y,w,h = rect
        # cv.rectangle(img_ori, (x,y), (x+w, y+h), (255,255,0), 20)
        # ROI = img_ori[y:y + h, x: x + w]
        # cv.imshow('ROI', ROI)
        # cv.waitKey(0)    

    crop = cv.bitwise_and(img_ori, img_ori, mask=mask)
    #crop feature for training
    # for c in cnt:
    #     x,y,w,h = cv.boundingRect(c)
    #     # threshhold on contour
    #     if w >= 30 and h >= 30:
                                                                                                                           #         cc = crop[y:y+w, x:x+h]
    #         cv.imshow('test', cc)
    #         cv.waitKey(0)
    # plt.subplot(2, 2, 1), plt.imshow(resizeWithAspectRatio(img_ori, 800))
    # plt.subplot(2, 2, 3), plt.imshow(resizeWithAspectRatio(mask, 800))
    # plt.subplot(2, 2, 4), plt.imshow(resizeWithAspectRatio(crop, 800))
    # plt.subplot(2, 2, 2), plt.imshow(resizeWithAspectRatio(img_lab, 800))
    # plt.show()
    # cv.imshow('Original', resizeWithAspectRatio(img_ori, 800))
    # cv.imshow('Mask', resizeWithAspectRatio(mask, 800))
    # cv.imshow('Cropped', resizeWithAspectRatio(crop, 800))
    # cv.imshow('Highlight', resizeWithAspectRatio(img_lab, 800))
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    SAVE_FILE_NAME_X = "x_train_data_%d.png"
    SAVE_FILE_NAME_Y = "y_train_data_%d.png"

    i = 1
    patch_size = 0
    for c in cnt:
        # draw a rectangle
        rect = cv.boundingRect(c)
        if rect[2] < 100 or rect[3] < 100: continue
        x,y,w,h = rect
        print(rect)

        patch_size = cal_crop_size(w,h)
        cc_img = img_ori[y:y + patch_size, x: x + patch_size,:]
        cc_msk = mask[y:y + patch_size, x: x + patch_size]
        # plt.subplot(1, 2, 1), plt.imshow(cc_img), plt.title("Data")
        # plt.subplot(1, 2, 2), plt.imshow(cc_msk), plt.title("Data")
        # plt.show()
        div_img(cc_img, cc_msk)
        i+=1

    # cv.destroyAllWindows()

def cal_crop_size(w,h):
    ps = max([w, h])
    print(ps)
    if ps // 1000 > 0:
        ps = int(math.ceil(ps / 1000) * 1000)
    else:
        ps = int(math.ceil(ps / 100) * 100)
    return ps
nn = 1
# #input, cropped image
def div_img(crop, mask):
    global nn
    patch_size = 200
    for i in range(0,crop.shape[0],patch_size):
        for j in range(0,crop.shape[1],patch_size):
            print("Here")
            cc = crop[i:i + patch_size, j:j + patch_size, :] # all ch
            cv.imwrite("dataset/train/asagao_%d.png" % nn, cc)
            cc = mask[i:i + patch_size, j:j + patch_size] # only bw
            cv.imwrite("dataset/validation/asagao_mask_%d.png" % nn, cc)
            nn += 1


test()
# test()

# #\\wsl$\Ubuntu-18.04\home\capilab\proj\opencv_asagau
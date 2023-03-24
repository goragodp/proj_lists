from glob import glob
from pickletools import optimize
import cv2 as cv
from PIL import Image
import PIL
IMG_FILES = sorted(glob('x_train_data*'))
MSK_FILES = sorted(glob('y_train_data*'))

X_SAVE_FILE_NAME = 'x_train_data_resized_%d.png'
Y_SAVE_FILE_NAME = 'y_train_data_resized_%d.png'
i = 1
for im, msk in zip(IMG_FILES, MSK_FILES):
    img = Image.open(im)
    mask = Image.open(msk)

    img_resize = img.resize((600,600), PIL.Image.NEAREST)
    msk_resize = mask.resize((600,600), PIL.Image.NEAREST)

    msk_resize.save(Y_SAVE_FILE_NAME % i, optimize=True, quality=100)
    img_resize.save(X_SAVE_FILE_NAME % i, optimize=True, quality=100)    
    i+=1
    # resize original image

# im = Image.open('x_train_data_1.png')
# im_resize = im.resize((500,500), PIL.Image.NEAREST)
# im_resize.save('resize_img.png',optimize=True, quality=80)
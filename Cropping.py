import numpy as np
from skimage.measure import label, regionprops

def crop(img, gt, crop_size):
    h,w = img.shape
    label_image = label(gt)
    ll = np.max(label_image)
    if ll > 1:
        print '---------error---------------'
    Img = []
    Gt =[]
#    Img=np.zeros([ll,crop_size])
#    Gt=np.zeros([ll,crop_size])
    for region in regionprops(label_image):
        cent = np.array(region.centroid)
        centerX = cent[0]
        centerY = cent[1]
        up = int(max(0, centerX-crop_size[0]/2))
        down = up + crop_size[0]
        if down > h:
            down = h
            up = down - crop_size[0]
            
        left = int(max(0,centerY-crop_size[1]/2))
        right = left +crop_size[1]
        if right > w:
            right = w
            left = right -crop_size[1]
        rectGt = gt[up:down,left:right]
        rectImg = img[up:down,left:right]

        Img.append(rectImg)
        Gt.append(rectGt)

    return Img, Gt
   
    
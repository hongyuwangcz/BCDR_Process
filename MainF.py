# organize all the data together;
import csv
import scipy.io as io
from PIL import Image, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
from Cropping import crop
from scipy import misc
import os
import PIL

F = ['F01','F02','F03']
FNAME=['BCDR-F01_dataset','BCDR-F02_dataset','BCDR-F03_dataset']
CSV = ['bcdr_f01_outlines.csv','bcdr_f02_outlines.csv','bcdr_f03_outlines.csv']
#csv_f = 'bcdr_f01_outlines.csv'

dir_img = './F/img'
dir_gt = './F/gt'
crop_size = [400,400]
Resize = [256,256]
Info_F = open('test.txt','w')

for i in range(3):
    dir_root = '../' + FNAME[i]
    csv_f = CSV[i]
    ff = F[i]
    with open(os.path.join(dir_root,csv_f)) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            flag = int(row['mammography_nodule'])
            if flag == 1:
                cla = row['classification']
                view = row['image_view']
                den = row['density']
        
                image_name = os.path.join(dir_root,row['image_filename'].lstrip( ))
                kernel,temp = os.path.splitext(row['image_filename'].split("/")[-1])
                im = Image.open(image_name)
                im = np.array(im)
                h,w = im.shape
                
                pX = row['lw_x_points']
                pX=pX.split()
                X =[int(x) for x in pX]
                    
                pY = row['lw_y_points']
                pY = pY.split()
                Y = [int(y) for y in pY]
    
                polygon = zip(X, Y)
                cell_mask = Image.new('L', (w, h), 0)
                ImageDraw.Draw(cell_mask).polygon(polygon, fill=255)
                
                gt = np.array(cell_mask)
                crop_img,crop_gt = crop(im,gt,crop_size)
                patchNum = 0
                for rr in range(len(crop_img)):
                    name = ff + '-' + kernel + '-'+ str("%03d" % patchNum) + '.png'             
                    saveImg = os.path.join(dir_img ,name)
                    saveGt = os.path.join(dir_gt ,name)
                    
                    Info_F.write(str(name)+' '+str(cla)+' ' + str(den) +' '+ str(view)+'\n')           
                    
                    RectImg = np.array(Image.fromarray(crop_img[rr]).resize((Resize[0],Resize[1]), PIL.Image.ANTIALIAS))          
                    RectGt = np.array(Image.fromarray(crop_gt[rr]).resize((Resize[0],Resize[1]), PIL.Image.ANTIALIAS))
        
                    RectGt[RectGt>150]=255
                    RectGt[RectGt<=150]=0
                                      
                    misc.imsave(saveImg, RectImg)
                    misc.imsave(saveGt, RectGt)                 
                    patchNum = patchNum + 1
Info_F.close()        

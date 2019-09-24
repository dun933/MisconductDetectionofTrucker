import os,re,cv2
import numpy as np

#Other
path = 'paper/'
save_folder = '../mlp-training/'
expansion_rate = 2

def expansion(img,bbox,rate):
    width = bbox[1] - bbox[0]
    height = bbox[3] - bbox[2]
    center = [bbox[0]+width/2,bbox[2]+height/2]
    
    new_bbox = [round(center[0] - (width/2)*rate), \
                round(center[0] + (width/2)*rate), \
                round(center[1] - (height/2)*rate), \
                round(center[1] + (height/2)*rate) ]
    img = img[new_bbox[2]:new_bbox[3], new_bbox[0]:new_bbox[1]]
    #print(center)
    #print(new_bbox)
    return img
    
for file in os.listdir(path+'annotation/'):
    label = 'paper-'
    image_path = path + 'images/' + file[:file.index('.xml')] + '.jpg'
    anno_path  = path + 'annotation/' + file
    img = cv2.imread(image_path)
    with open(anno_path,'r+') as f:
        content = f.read()
        
        xmin = int(re.findall('<xmin>(.*?)</xmin>', content)[0])
        xmax = int(re.findall('<xmax>(.*?)</xmax>', content)[0])
        ymin = int(re.findall('<ymin>(.*?)</ymin>', content)[0])
        ymax = int(re.findall('<ymax>(.*?)</ymax>', content)[0])
        #print(file,[xmin,xmax,ymin,ymax])
        img = expansion(img,[xmin,xmax,ymin,ymax],expansion_rate)
        f.close()
    #print(img[ymin:ymax,xmin:xmax])    
    # cv2.imwrite(save_folder+label+file[:file.index('.xml')]+'.jpg',img)
    cv2.imwrite(save_folder+label+file[:file.index('.xml')]+'.jpg',img)

    
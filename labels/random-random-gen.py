import os, cv2
import random as rd
path = 'random/'
save_folder_anno = path+'annotation/'
save_folder_images = path+'crop_images/'

def gen_bbox(height,width):
    # new_height = rd.randint(1,height-50)
    # new_width = new_height
    new_height = 100
    new_width = 100
    # new_width = rd.randint(1,width-50)
    position = (rd.randint(1,height-new_height), rd.randint(1,width-new_width))
    return position, new_height, new_width
    
for file in os.listdir(path+'images/'):
    img = cv2.imread(path+'images/'+file)
    height, width = img.shape[0], img.shape[1]
    position, height, width = gen_bbox(height, width)
    with open(save_folder_anno+file[:file.index('.')]+'.xml','w+') as f:
        f.write('<xmin>'+str(position[0])+'</xmin>')
        f.write('<ymin>'+str(position[1])+'</ymin>')
        f.write('<xmax>'+str(position[0]+width)+'</xmax>')
        f.write('<ymax>'+str(position[1]+height)+'</ymax>')
        f.close()
    cv2.imwrite(save_folder_images+file, img[   position[0]:position[0]+width,
                                                position[1]:position[1]+height  ])

    
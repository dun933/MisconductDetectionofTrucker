import re,os
#replacement setting
#anno = 'closebaffle/annotation/'
anno = 'labels/paper/annotation/'
folder = 'labels/cup/images'




for file in os.listdir(anno):
    path = '../images/'+file[:file.index('.xml')]+'.jpg'
    #path = folder+'/'+file[:file.index('.xml')]+'.jpg'
    with open(anno+file,'r+') as f:
            content = f.read()
            f.close()
    #content = re.sub('<folder>(.*?)</folder>', '<folder>'+folder+'</folder>',content)
    content = re.sub('<path>(.*?)</path>', '<path>'+path+'</path>',content)
    with open(anno+file,'w') as f:
            f.write(content)
            f.close()

'''
 @author  lijianqing
 @date  2023/3/17 下午1:41
 @version 1.0
'''

from labelme.utils import shape as shape_labelme
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
import numpy as np
import json
import multiprocessing
import glob
from labelme.utils import shape as shape_labelme
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
from labelme.utils import shape as shape_labelme
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
import numpy as np
import json
import multiprocessing
import glob
import time
class labelme2coco(object):
    def __init__(self,labelme_json=[],save_json_path='./new.json',resume_cate = None):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.labelme_json=labelme_json
        self.save_json_path=save_json_path
        self.height=0
        self.width=0
        self.save_json()
    def addshape(self,shape,data,num,annotations,categories,labels):
        label=shape['label'].split('_')
        # print('label',label[0],'labels:',labels,'--')
        if label[0] not in labels:
            # print(categories,'c---')
            labels.append(label[0])
            categories.append(self.categorie(label,labels))
            # print(categories,'c---1')
        # print('label1',label,'labels:',labels,'--')
        points=shape['points']
        w = data['imageWidth']
        h =data['imageHeight']
        shape_type =shape['shape_type']
        img_shape = (h,w, 3)
        annotations.append(self.annotation(img_shape,points,label,num,shape_type,annotations,categories))

    def data_transfer1(self):
        pool = multiprocessing.Pool(processes=32) # 创建进程个数
        images = []
        #images=multiprocessing.Manager().list()
        annotations = multiprocessing.Manager().list()
        print('anno',annotations)
        categories = multiprocessing.Manager().list()
        labels = multiprocessing.Manager().list()
        for num,json_file in enumerate(self.labelme_json):
            with open(json_file,'r',encoding='utf-8') as fp:
                print('json_file:---',json_file)
                data = json.load(fp)  # json
                #print('data',data)
                images.append(self.image(data,num))
                for shape in data['shapes']:
                    print('len(annotations)',len(annotations))
                    pool.apply_async(self.addshape,args=(shape,data,num,annotations,categories,labels))
        pool.close()
        pool.join()


        return (images,annotations,categories)

    def data_transfer(self):
        pool = multiprocessing.Pool(processes=32)  # 创建进程个数
        images = []
        # images=multiprocessing.Manager().list()
        annotations = []
        categories = []
        labels =[]
        sum_=0
        for num, json_file in enumerate(self.labelme_json):
            with open(json_file, 'r', encoding='utf-8') as fp:
                print('json_file:---', json_file)
                data = json.load(fp)  # json
                images.append(self.image(data, num))
                for shape in data['shapes']:
                    sum_+=1
                    print('len(annotations)', len(annotations))
                    self.addshape(shape, data, num, annotations, categories, labels)
        print('sum_',sum_)
        return (images, annotations, categories)

    def image(self,data,num):
        image={}
        height,width = data["imageHeight"],data["imageWidth"]
        image['height']=height
        image['width'] = width
        image['id']=num+1
        image['file_name'] = data['imagePath'].split('/')[-1]

        self.height=height
        self.width=width

        return image

    def categorie(self,label,labels):
        categorie={}
        categorie['supercategory'] = label[0]
        categorie['id']=len(labels)-1#+1 # 0 默认为背景
        categorie['name'] = label[0]
        return categorie

    def annotation(self,img_shape,points,label,num,shape_type,annotations,categories):
        annotation={}
        try:
            if len(points)==2:
                shape_type='rectangle'
            mask = shape_labelme. shape_to_mask(img_shape[:2], points,shape_type)
            annotation['bbox'] = list(map(float,self.mask2box(mask)))
            mask =mask+0
            # print('img_shape, data["shapes"]',img_shape,shape_type,np.shape(mask))
            mask=np.asfortranarray(mask).astype('uint8')
            segm = encode(mask)#编码为rle格式
            annotation['area'] = float(maskUtils.area(segm))#计算mask编码的面积，必须放置在mask转字符串前面，否则计算为0
            segm['counts'] = bytes.decode(segm['counts'])#将字节编码转为字符串编码
            annotation['segmentation']=segm
            annotation['iscrowd'] = 0
            annotation['image_id'] = num+1
            # print('categories',categories)
            annotation['category_id'] = self.getcatid(label,categories)
            annotation['id'] = len(annotations)+1
        except Exception as e:
            print('points:',points)
        return annotation

    def getcatid(self,label,categories):
        for categorie in categories:
            if label[0]==categorie['name']:
                return categorie['id']
        return -1

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)
        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def data2coco(self,images,annotations,categories):
        # print(annotations,'===',type(annotations))
        # print(list(categories),'===',type(list(categories)))
        data_coco={}
        data_coco['images']=images
        data_coco['categories']=list(categories)
        data_coco['annotations']=list(annotations)
        print('len_:',len(list(annotations)))
        return data_coco

    def save_json(self):
        # print('save')
        images,annotations,categories=self.data_transfer()
        # print('images',images)
        # print('annotations',annotations)
        print('categories',categories)
        data_coco = self.data2coco(images,annotations,categories)
        #print(data_coco)
        # # 保存json文件
        json.dump(data_coco, open(self.save_json_path, 'w',encoding='utf-8'), indent=4)

if __name__ == '__main__':

    labelme_json=glob.glob('/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_cropped768/val/original_ipad/*.json')
    coco_path = 'instances_val2017.json'
    labelme2coco(labelme_json,coco_path)
from labelme import utils
import multiprocessing
import json
import time
import cv2
import os
import shutil
import glob
class ToMaskLabel(object):
    def __init__(self,cut_jsons_path,class_mapers,save_mask_path,save_seg_label_path,mask_except,process_nums=32):
        self.cut_jsons_path = cut_jsons_path
        self.class_mapers = class_mapers
        self.save_mask_path = save_mask_path
        self.save_seg_label_path = save_seg_label_path
        self.process_nums = process_nums
        self.mask_except = mask_except

        if not os.path.exists(save_mask_path):
            os.makedirs(save_mask_path)
        if not os.path.exists(save_seg_label_path):
            os.makedirs(save_seg_label_path)
        if not os.path.exists(mask_except):
            os.makedirs(mask_except)
        self.main()
        print(0)
    def main(self):
        input_ts = []
        for file_name in os.listdir(self.cut_jsons_path):
            json_p = os.path.join(self.cut_jsons_path,file_name)
            if file_name.endswith('.json'):
                name = file_name.split('.json')[0]
                r_mask = os.path.join(self.save_mask_path,name)
                r_label = os.path.join(self.save_seg_label_path,name)
                r_mask_except = os.path.join(self.mask_except,name)
                input_ts.append((json_p,r_mask,r_label,r_mask_except))
        pool = multiprocessing.Pool(processes=self.process_nums) # 创建进程个数
        pool.map(self.toMaskLabel,input_ts)
        pool.close()
        pool.join()
    def toMaskLabel(self,input):
        json_file,r_mask,r_label,mask_except = input
        data = json.load(open(json_file,encoding='utf8'))
        img_shape = (data['imageHeight'],data['imageWidth'],3)
        #img_shape = (data['imageHeight'],data['imageWidth'],data['imageDepth'])
        try:
            lbl, _ = utils.shapes_to_label(img_shape, data["shapes"], self.class_mapers)
            utils.lblsave(r_mask, lbl)
            img_data = cv2.imread('{}.png'.format(r_mask))
            img_data_grey = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('{}.png'.format(r_label), img_data_grey)
            print('正在处理：',r_label,json_file)
        except:
            shutil.move(json_file,'{}.json'.format(mask_except))
            print('异常处理：',json_file)
if __name__ == '__main__':
    # class_mapers ={'a': 0,'aokeng': 1, 'aotuhen': 2, 'baisezaodian': 3, 'cashang': 4, 'daowen': 5, 'guashang': 6, 'heidian': 7, 'huanxingdaowen': 8,
    #                'maoxu': 9, 'mianhua': 10, 'pengshang': 11, 'penshabujun': 12,'shahenyin': 13, 'shuiyin': 14, 'tabian': 15, 'yise': 16, 'yiwu': 17}
    # class_mapers ={'a': 0,'aokeng':1, 'baisezaodian':2, 'daowen':3, 'diaoqi':4,'guashang':5, 'heidian':6, 'pengshang':7, 'shahenyin':8, 'tabian':9,
    #                 'yise':10, 'yiwu':11,'guoqie':12,'3ddaowen':13,'cashang':14}
    class_mapers = {'lp': 0, 'aokeng': 1, 'aotuhen': 2, 'baisezaodian': 3, 'daowen': 4, 'guashang': 5,
                    'heidian': 6, 'huanxingdaowen': 7, 'mianhua': 8,
                    'pengshang': 9,'penshabujun': 10, 'shahenyin': 11, 'tabian': 12, 'yise': 13, 'yiwu': 14, 'guoqie': 15,
                    'cashang': 16, '3ddaowen': 17}
    class_mapers ={'huashang': 1, 'pengshang': 2, 'yashang': 3, 'aotu': 4}
    #r

    #class_mapers ={'a': 0,'heidian':1, 'baisezaodian':2,}#{'a': 0,'aokeng':1, 'aotuhen':2, 'baisezaodian':3, 'daowen':4,'guashang':5, 'heidian':6, 'huanxingdaowen':7, 'mianhua':8, 'pengshang':9,
                   # 'penshabujun':10, 'shahenyin':11,'tabian':12,'yise':13,'yiwu':14}

    cut_jsons_path = "/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/coco_768/train2017"
    mask = "/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/coco_768/train2017_mask"
    import os
    if not os.path.exists(mask):
        os.makedirs(mask)
    save_seg_label_path = "/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/coco_768/train2017_labels"
    if not os.path.exists(save_seg_label_path):
        os.makedirs(save_seg_label_path)
    mask_except = "./excepts"
    s = time.time()
    tomasklabel = ToMaskLabel(cut_jsons_path=cut_jsons_path,class_mapers=class_mapers,save_mask_path=mask,
                              save_seg_label_path=save_seg_label_path,mask_except=mask_except,process_nums=32)
    print('tomask_label:',time.time()-s)
    #['aokeng', 'aotuhen', 'baisezaodian', 'cashang', 'daowen', 'guashang', 'heidian', 'huanxingdaowen', 'maoxu',
    #  'mianhua', 'pengshang', 'penshabujun', 'shahenyin', 'shuiyin', 'tabian', 'yise', 'yiwu']
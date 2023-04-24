# ---------------------------class2----------------------start
#切除图像多余边框
import json
import os
import cv2
'''
@Description: 
            主要功能：切除非光学面区域
            关键处理：有标注切除，无标注切除
@author: lijianqing
@date: 2020/11/24 16:45
@return 

@param: 输入：数据存放路径，root_path 
             切除后数据保存路径：out_path（不存在的时候会自动创建）
             切图的起点位置：start_point=[96,46] 
             切图宽高：crop_w = 3308,crop_h = 4854
             切图是否有标注：anno=True，没有标注时为False
'''
class Cut_edge(object):
    def __init__(self,root_path,out_path,start_point=[96,46],crop_w = 3308,crop_h = 4854,anno=True):
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        for i in os.listdir(root_path):
            if anno:
                if i.endswith('.json'):
                    jsons_path = os.path.join(root_path,i)
                    print('正在处理：',jsons_path)
                    self.cut_json(jsons_path,root_path,out_path,start_point,crop_w,crop_h)
            else:
                if i.endswith('.jpg'):
                    img_n = os.path.join(root_path,i)#原图像名
                    img_np = cv2.imread(img_n)#原图数据
                    self.save_new_img(img_np,i,start_point[0],start_point[1],start_point[0]+crop_w,start_point[1]+crop_h,out_path)

    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
    def save_new_img(self,img_np,img_name,xmin,ymin,xmax,ymax,out_path):
        # 切图并保存
        xmin,ymin,xmax,ymax = int(xmin),int(ymin),int(xmax),int(ymax)
        # img_h, img_w, d=img_np.shape
        # pading_r=2240-img_w
        # pading_d=3036-img_h
        # left,top,right,down = 0,0,pading_r,pading_d#need padding size
        img_crop = img_np[ymin:ymax,xmin:xmax]
        #ret = cv2.copyMakeBorder(img_crop, top, down, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))#padding
        #cv2.imwrite(os.path.join(out_path, img_name), img_crop)
        cv2.imwrite(os.path.join(out_path, img_name), img_crop)
        return 0
    def get_new_location(self,point,start_point):
        return [point[0]-start_point[0],point[1]-start_point[1]]

    def cut_json(self,json_p,img_sourc,out_path,start_point,w,h):
        with open(json_p, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        img_n = os.path.join(img_sourc,json_data['imagePath'])#原图像名
        img_np = cv2.imread(img_n)#原图数据
        json_data['imageHeight']=h
        json_data['imageWidth']=w

        for index_object in json_data['shapes']:
            points = index_object['points']
            new_points = []
            x_list = []
            y_list = []
            in_crop_flag=False
            for i in points:

                n_p = self.get_new_location(i,start_point)
                x, y = n_p
                if x < w and y < h and x>0 and y>0:
                    new_points.append(n_p)
                    in_crop_flag=True
                else:
                    if x>w:
                        x=w
                    if y>h:
                        y=h
                    if x<0:
                        x=0
                    if y<0:
                        y=0
                    new_points.append([x,y])

                x_list.append(x)
                y_list.append(y)

            if index_object['shape_type']=='circle':
                if len(new_points)!=2:
                    new_points=[]
            if not in_crop_flag:
                if max(x_list)==min(x_list) or max(y_list)==min(y_list):
                    new_points = []
            print('--',index_object['label'],new_points)

            index_object['points']=new_points
        self.save_new_img(img_np,json_data['imagePath'],start_point[0],start_point[1],start_point[0]+w,start_point[1]+h,out_path)
        new_name_json = json_data['imagePath'].replace('jpg','json')
        self.save_json(json_data,os.path.join(out_path,new_name_json))


# ---------------------------class2----------------------end
if __name__ == '__main__':
    test_root_path = '/home/lijq/Desktop/test'
    out_path = os.path.join(test_root_path, 'cut_edge')
    Cut_edge(test_root_path, out_path, start_point=[100, 100], crop_w=2224, crop_h=1824, anno=True)
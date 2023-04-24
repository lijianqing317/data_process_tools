import json
import cv2
import glob
import cv2
import os
# import pandas as ps
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic
# def read_csv(csv_path):
#     r = ps.read_csv(csv_path,usecols=['class_name','xmin','ymin','bb_width','bb_height','score'])
#     return r
def draw_bbox(img,left_top,right_down,color,label):
    cv2.rectangle(img, left_top, right_down, color,5)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, label, left_top, font, 1, color, 5)
    return img

def iter_dic(source_p,save_p):
    img_p_s = glob.glob('{}/{}'.format(source_p,'*.jpg'))
    r_s = glob.glob('{}/{}'.format(source_p,'*.json'))
    for i in range(len(img_p_s)):
        name = img_p_s[i].split('/')[-1]
        print('name',name)
        img = cv2.imread(img_p_s[i])
        r = parse_para(img_p_s[i].replace('jpg','json'))
        shapes=r['shapes']
        for shape in shapes:
            l,t=shape['points'][0]
            l_t=(int(l),int(t))
            r,d=shape['points'][1]
            r_d=(int(r),int(d))
            lable='{}:{}'.format(shape['label'],"%.2f" %shape['score'])
            color = (0, 0, 255)
            img = draw_bbox(img, l_t, r_d, color, lable)
            # print('img',img)
        # for j in range(len(shapes)):
        #     l_t=(int(r['xmin'][j]),int(r['ymin'][j]))
        #     r_d = (int(r['xmin'][j])+int(r['bb_width'][j]),int(r['ymin'][j])+int(r['bb_height'][j]))
        #     lable = '{}:{}'.format(r['class_name'][j],"%.2f" %r['score'][j])
        #     color = (0,192,255)
        #     img=draw_bbox(img, l_t, r_d,color, lable)
        cv2.imwrite(os.path.join(save_p,name),img)
if __name__ == '__main__':

    s_path = '/home/lijq/Desktop/data/byd/workspace/byd_ipad_workspace/train_val_data/test/IPAD-12'#csv 和 img
    save_p = '/home/lijq/Desktop/IPAD-12_r1'#结果img
    print(os.path.exists(save_p))
    if not os.path.exists(save_p):
        print(os.path.exists(save_p))
        os.makedirs(save_p)
iter_dic(s_path,save_p)
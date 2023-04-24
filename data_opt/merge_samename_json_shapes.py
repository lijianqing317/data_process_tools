'''
 @author  lijianqing
 @date  2023/3/14 下午5:24
 @version 1.0
'''
import json
import argparse
import os
import numpy as np
def parse_para(input_json):
    with open(input_json, "r", encoding="utf-8") as f:
        ret_dic = json.load(f)
    return ret_dic


def save_json(dic, save_path):
    json.dump(dic, open(save_path, "w", encoding="utf-8"), indent=4)

input_gt='/home/lijq/Desktop/data/byd/test/gt'
input_overkill='/home/lijq/Desktop/data/byd/test/loushi1/over'
out_path='/home/lijq/Desktop/data/byd/test/loushi1/over'
if not os.path.exists(out_path):
    os.makedirs(out_path)
for gt_file in os.listdir(input_gt):
    if gt_file.endswith('json'):
        gt_file_path=os.path.join(input_gt,gt_file)
        gt_data=parse_para(gt_file_path)
        print('gt_file_path',gt_file_path)
        gt_shapes = gt_data['shapes']
        try:
            pre_data = parse_para(gt_file_path.replace(input_gt, input_overkill))
            pre_shapes=pre_data['shapes']
            gt_shapes.extend(pre_shapes)
        except:
            print('不存在过检')
        gt_data['shapes']=gt_shapes
        save_json(gt_data,gt_file_path.replace(input_gt,out_path))

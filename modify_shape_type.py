'''
 @author  lijianqing
 @date  2023
 @version 1.0
'''
import json
import os
def parse_para(input_json):
    with open(input_json, "r", encoding="utf-8") as f:
        ret_dic = json.load(f)
    return ret_dic


def save_json(dic, save_path):
    json.dump(dic, open(save_path, "w", encoding="utf-8"), indent=4)

input_gt='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/workspace_0407/train_val_data/val/original_ipad'
out_path='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/workspace_0407/train_val_data/val/original_ipad'
if not os.path.exists(out_path):
    os.makedirs(out_path)
for gt_file in os.listdir(input_gt):
    if gt_file.endswith('json'):
        gt_file_path=os.path.join(input_gt,gt_file)
        gt_data=parse_para(gt_file_path)
        print('gt_file_path',gt_file_path)
        gt_shapes = gt_data['shapes']
        new_shapes=[]
        for shape in gt_shapes:
            if shape['shape_type'] == 'linestrip':
                shape['shape_type'] = 'polygon'
            new_shapes.append(shape)
        gt_data['shapes']=new_shapes
        save_json(gt_data,gt_file_path.replace(input_gt,out_path))
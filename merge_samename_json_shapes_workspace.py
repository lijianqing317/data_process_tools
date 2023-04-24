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


def args_para():
    parser = argparse.ArgumentParser(description="modify name and filter class")
    parser.add_argument("--workspace", type=str,default='/home/lijq/Desktop/data/O_ALL/workspace_single')
    parser.add_argument("--data_gt", type=str,default='data_GT_no_miss_jsons')
    parser.add_argument("--data_overkill",type=str,default='data_no_topk_jsons')
    parser.add_argument("--data_save",type=str,default='data_merge_gtnomiss_notopkoverkill')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = args_para()
    workspace = args.workspace
    data_gt = os.path.join(workspace, args.data_gt)
    data_overkill = os.path.join(workspace, args.data_overkill)
    data_save = os.path.join(workspace, args.data_save)
    for train_val_file in os.listdir(data_gt):
        sub_train_val_file = os.path.join(data_gt, train_val_file)
        for data_batch_name in os.listdir(sub_train_val_file):
            data_batch_file = os.path.join(sub_train_val_file, data_batch_name)
            input_gt = data_batch_file
            input_overkill = data_batch_file.replace(data_gt, data_overkill)
            input_save_gt_merge = data_batch_file.replace(data_gt, data_save)

            input_gt=input_gt
            input_overkill=input_overkill
            out_path=input_save_gt_merge

            # input_gt='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data/train/original_ipad'
            # input_overkill='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data/train/original_ipad_guosha_no_topk'
            # out_path='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data/train/original_ipad_merge_not_topk_overkill'
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

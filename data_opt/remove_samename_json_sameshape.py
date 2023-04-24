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
    parser.add_argument("--input_overkill", type=str,default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/byd_ipad_workspace/train_val_data_cropped/train/original_ipad_preatssyolov8_loushi/0.1/over')
    parser.add_argument("--input_overkill_top", type=str,default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/byd_ipad_workspace/train_val_data_cropped/train/original_ipad_preatssyolov8_loushi/0.3/over')
    parser.add_argument("--input_overkill_no_top",type=str,default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/byd_ipad_workspace/train_val_data_cropped/train/filter_dataset/overkill0.1-0.3')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args=args_para()
    # input_overkill='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_croped/train/crop_ipad'
    # input_overkill_top='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_croped/train/_loushi/0.1/over'
    # input_overkill_no_top='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_croped/train/_loushi/0.1/merge_over'
    input_overkill=args.input_overkill
    input_overkill_top=args.input_overkill_top
    input_overkill_no_top=args.input_overkill_no_top
    if not os.path.exists(input_overkill_no_top):
        os.makedirs(input_overkill_no_top)
    for overkill_file in os.listdir(input_overkill):
        if overkill_file.endswith('json'):
            overkill_file_path=os.path.join(input_overkill,overkill_file)
            overkill_data=parse_para(overkill_file_path)
            print('gt_file_path',overkill_file_path)
            overkill_data_shapes = overkill_data['shapes']
            try:
                pre_data = parse_para(overkill_file_path.replace(input_overkill, input_overkill_top))
                pre_shapes=pre_data['shapes']
                for top_shape in pre_shapes:
                    if top_shape in overkill_data_shapes:
                        overkill_data_shapes.remove(top_shape)
            except:
                print('不存在topk数据')
                save_json(overkill_data, overkill_file_path.replace(input_overkill, input_overkill_no_top))
            overkill_data['shapes']=overkill_data_shapes
            save_json(overkill_data,overkill_file_path.replace(input_overkill,input_overkill_no_top))

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
    parser.add_argument("--data", type=str,default='data')
    parser.add_argument("--data_select",type=str,default='data_miss')
    parser.add_argument("--data_no_select",type=str,default='data_no_miss')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args=args_para()
    workspace=args.workspace
    data=os.path.join(workspace,args.data)
    data_select=os.path.join(workspace,args.data_select)
    data_no_select=os.path.join(workspace,args.data_no_select)
    for train_val_file in os.listdir(data_select):
        sub_train_val_file=os.path.join(data_select,train_val_file)
        for data_batch_name in os.listdir(sub_train_val_file):
            data_batch_file=os.path.join(sub_train_val_file,data_batch_name)
            input_overkill=data_batch_file.replace(data_select,data)
            input_overkill_top=data_batch_file
            input_overkill_no_top=data_batch_file.replace(data_select,data_no_select)
            print(input_overkill)
            print(input_overkill_top)
            print(input_overkill_no_top)


            # input_overkill='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_croped/train/crop_ipad'
            # input_overkill_top='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_croped/train/_loushi/0.1/over'
            # input_overkill_no_top='/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_croped/train/_loushi/0.1/merge_over'
            # input_overkill=args.input_overkill
            # input_overkill_top=args.input_overkill_top
            # input_overkill_no_top=args.input_overkill_no_top

            if not os.path.exists(input_overkill_no_top):
                os.makedirs(input_overkill_no_top)
            for overkill_file in os.listdir(input_overkill):
                if overkill_file.endswith('json'):
                    overkill_file_path=os.path.join(input_overkill,overkill_file)
                    overkill_data=parse_para(overkill_file_path)
                    # print('gt_file_path',overkill_file_path)
                    overkill_data_shapes = overkill_data['shapes']
                    try:
                        pre_data = parse_para(overkill_file_path.replace(input_overkill, input_overkill_top))
                        pre_shapes=pre_data['shapes']
                        for top_shape in pre_shapes:
                            # print('keys',dict(top_shape).keys())
                            # print('keys',dict(overkill_data_shapes[0]).keys())
                            # difference_list=list(set(dict(top_shape).keys()).difference(set(dict(overkill_data_shapes[0]).keys())))
                            # #intersection_list=list(set(dict(top_shape).keys()).intersection(set(dict(overkill_data_shapes[0]).keys())))
                            # # del top_shape[i] for i in difference_list
                            # for diff_key in difference_list:
                            #     del top_shape[diff_key]
                            # print('keys--', dict(top_shape).keys())
                            # print('keys---', dict(overkill_data_shapes[0]).keys())
                            # if top_shape in overkill_data_shapes:
                            #     overkill_data_shapes.remove(top_shape)
                            for selecet_shape_ in overkill_data_shapes:
                                print('keys--', top_shape['points'])
                                print('keys---', selecet_shape_['points'])
                                print('keys--', dict(top_shape).keys())
                                print('keys---', dict(selecet_shape_).keys())
                                print('sppoints',top_shape['points']==selecet_shape_['points'])
                                print('slabels',top_shape['label']==selecet_shape_['lable'])
                                if top_shape['points']==selecet_shape_['points'] and top_shape['label']==selecet_shape_['lable']:
                                    overkill_data_shapes.remove(top_shape)

                    except:
                        print('不存在topk数据',overkill_file_path)
                        save_json(overkill_data, overkill_file_path.replace(input_overkill, input_overkill_no_top))
                    overkill_data['shapes']=overkill_data_shapes
                    save_json(overkill_data,overkill_file_path.replace(input_overkill,input_overkill_no_top))
                    ''''''

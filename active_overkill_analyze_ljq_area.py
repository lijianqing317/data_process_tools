'''
Author: qianzhiming
Date: 2023-02-03 13:56:50
LastEditTime: 2023-02-06 13:11:07
'''
'''
 @author  lijianqing
 @date  2023/2/2 上午11:45
 @version 1.0
'''
import json
import argparse
import os
import numpy as np

from mtl.utils.data_util import get_json_data, compute_iou, get_topk_guosha
from mtl.utils.selectfile_util import select_same_name_file


def process_pre_score_json_data(pre_json_data, args):
    guosha_shape_list = []
    for pre_shape in pre_json_data['shapes']:
        points = pre_shape["points"]
        pre_score = pre_shape['score']
        pre_label = pre_shape['label']
        #if pre_label in args.class_score_dic and pre_score >= args.class_score_dic[pre_label]:
        #score:
        # if pre_score >= args.class_score_dic['other']:
        min_score,max_sorce=args.class_score_dic['other']
        # if pre_score > min_score and pre_score < max_sorce:
        #     guosha_shape_list.append(pre_shape)
        gt_min_x, gt_max_x, gt_min_y, gt_max_y = min(np.array(points)[:, 0]), max(
            np.array(points)[:, 0]), min(np.array(points)[:, 1]), max(np.array(points)[:, 1])
        w = gt_max_x - gt_min_x
        h = gt_max_y - gt_min_y

        # score_=shape['score']
        # if shape['label']==label:
        #if w*h>=500 and w*h<5000:
        if w*h>50000:
            guosha_shape_list.append(pre_shape)

    guosha_json_data = pre_json_data
    guosha_json_data['shapes'] = guosha_shape_list
    return guosha_json_data

def process_pre_iou_under_gt_json_data(gt_json_data, pre_json_data, args):
    guosha_shape_list = []
    for pre_shape in pre_json_data['shapes']:
        pre_points = pre_shape["points"]
        pre_min_x, pre_max_x, pre_min_y, pre_max_y = min(np.array(pre_points)[:, 0]), max(
            np.array(pre_points)[:, 0]), min(np.array(pre_points)[:, 1]), max(np.array(pre_points)[:, 1])
        pre_score = pre_shape['score']
        max_iou = 0
        label = "other"
        for gt_shape in gt_json_data['shapes']:
            gt_points = gt_shape["points"]
            gt_min_x, gt_max_x, gt_min_y, gt_max_y = min(np.array(gt_points)[:, 0]), max(
                np.array(gt_points)[:, 0]), min(np.array(gt_points)[:, 1]), max(np.array(gt_points)[:, 1])
            iou_value = compute_iou(pre_min_x, pre_max_x, pre_min_y, pre_max_y, gt_min_x, gt_max_x, gt_min_y, gt_max_y)
            # print('iou',iou_value,gt_shape['label'])
            # print('shape:',gt_shape)
            # print('pre_shape:',pre_shape)
            if iou_value > max_iou:
                max_iou = iou_value
                label = gt_shape['label']

        if not label in args.class_score_dic:
            label = 'other'
        if max_iou < args.class_iou_dic[label]:
            if args.score_flag:
                if pre_score >= args.class_score_dic[label]:
                    guosha_shape_list.append(pre_shape)
            else:
                guosha_shape_list.append(pre_shape)
        else:
            continue
    guosha_json_data = pre_json_data
    guosha_json_data['shapes'] = guosha_shape_list
    return guosha_json_data


def main(args):
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    for pre_json_basename in os.listdir(args.pre_json_dir):
        if pre_json_basename.endswith('json'):
            pre_json_path = os.path.join(args.pre_json_dir, pre_json_basename)
            print('正在处理：', pre_json_path)
            pre_json_data = get_json_data(pre_json_path)
            if args.lp_flag:
                guosha_json_data = process_pre_score_json_data(pre_json_data, args)
                if len(guosha_json_data['shapes']) != 0:
                    json.dump(guosha_json_data,
                              open(pre_json_path.replace(args.pre_json_dir, args.save_dir), 'w', encoding='utf-8'),
                              indent=4)
                    # if args.copy_img:
                    #     select_same_name_file(args.save_dir, 'json', args.pre_json_dir, args.save_dir, ['jpg'], True)
            else:
                gt_json_list = os.listdir(args.gt_json_dir)
                if pre_json_basename in gt_json_list:
                    gt_json_path = os.path.join(args.gt_json_dir, pre_json_basename)
                    gt_json_data = get_json_data(gt_json_path)
                    guosha_json_data = process_pre_iou_under_gt_json_data(gt_json_data, pre_json_data, args)
                    if len(guosha_json_data['shapes']) != 0:
                        json.dump(guosha_json_data, open(pre_json_path.replace(args.pre_json_dir, args.save_dir), 'w', encoding='utf-8'), indent=4)
                else:
                    print("未找到匹配的json！", pre_json_path)

    get_topk_guosha(gs_path=args.save_dir, topk=args.top_k, gs_topk_path=args.gs_topk_path)
    if args.copy_img:
        select_same_name_file(args.save_dir,'json',args.gt_json_dir,args.save_dir,['jpg'],True)
        select_same_name_file(args.gs_topk_path,'json',args.gt_json_dir,args.gs_topk_path,['jpg'],True)

def get_parser():
    all={'other': 0.2}
    parser = argparse.ArgumentParser(description="The tool used to analyze overkill data.")
    parser.add_argument("--gt_json_dir", default='', type=str, help="")
    parser.add_argument("--pre_json_dir", default='/home/lijq/Desktop/data/O_ALL/workspace_lp/data_pre/olp327_no0.2topk_jsons_bk', type=str, help="")
    parser.add_argument("--save_dir", default='/home/lijq/Desktop/data/O_ALL/workspace_lp/data_pre/olp327_no0.2topk', type=str, help="")
    parser.add_argument("--class_iou_dic", default={'other': [0.01,0.051]}, type=dict, help="")
    parser.add_argument("--class_score_dic", default={'other': [0.01,0.051]}, type=dict, help="")
    parser.add_argument("--score_flag", default=True, type=bool, help="")
    parser.add_argument("--top_k", default=50000000, type=int, help="")
    parser.add_argument("--gs_topk_path", default='/home/lijq/Desktop/data/O_ALL/workspace_lp/data_pre/olp327_no0.2topk', type=str, help="")
    parser.add_argument("--copy_img", default=True, type=bool, help="")
    parser.add_argument("--lp_flag", default=True, type=bool, help="")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    '''使用说明：挑选过杀数据
    '''
    args = get_parser()
    main(args)

    if args.copy_img:
        select_same_name_file(args.save_dir,'json',args.gt_json_dir,args.save_dir,['jpg'],True)

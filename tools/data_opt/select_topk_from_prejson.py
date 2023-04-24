'''
 @author  lijianqing
 @date  2023/3/23 下午12:20
 @version 1.0
'''
import os
import argparse
import json
import glob
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic

def counter_cate(json_path):
    jsons = glob.glob('{}/*.json'.format(json_path))
    classes_dic = {}
    for i in jsons:
        ret_dic = parse_para(i)
        shapes = ret_dic['shapes']
        for j in shapes:
            if j['label'] not in classes_dic:
                classes_dic[j['label']] = 1
            else:
                classes_dic[j['label']] += 1
    counter_sort = sorted(classes_dic.items(),key=lambda x:x[1],reverse=True)
    print('缺陷名排序',sorted(list(classes_dic.keys())))
    print('缺陷数量排序',counter_sort)
    print('缺陷种类',len(counter_sort))
    sum = 0
    for i in classes_dic:
        sum += classes_dic[i]
    print('目标汇总数：',sum)
    print(classes_dic)
    dic_ = {}
    for i in list(classes_dic.keys()):
        dic_[i] = str(i).split('-')[0]
    print(dic_)
    return sum

def get_topk_guosha(gs_path, topk, gs_topk_path):  # 在所有过杀数据里挑topk过杀数据
    if not os.path.exists(gs_topk_path):
        os.makedirs(gs_topk_path)
    # 不区分类别
    topk_list = []
    topk_shape_list = []
    topk_json_path_list = []
    topk_json_data_list = []
    min_score = 1
    min_index = -1
    for gs_path_basename in os.listdir(gs_path):
        if gs_path_basename.endswith('json'):
            print("正在处理：", gs_path_basename)
            gs_json_path = os.path.join(gs_path, gs_path_basename)
            with open(gs_json_path, 'r', encoding='utf-8') as fgs:
                gs_data = json.load(fgs)
            data_shapes = gs_data.pop('shapes', [])
            for shape in data_shapes:
                score = shape['score']
                if len(topk_list) < topk:
                    topk_list.append(score)
                    topk_shape_list.append(shape)
                    topk_json_data_list.append(gs_data)
                    topk_json_path_list.append(gs_path_basename)
                    if score < min_score:
                        min_score = score
                        min_index = len(topk_list) - 1
                else:
                    if score > min_score:
                        topk_list[min_index] = score
                        topk_shape_list[min_index] = shape
                        topk_json_data_list[min_index] = gs_data
                        topk_json_path_list[min_index] = gs_path_basename
                        min_score = min(topk_list)
                        min_index = topk_list.index(min_score)

    # 将topk shape保存
    json_path_shape_dic = {}
    json_path_data_dic = {}
    for index in range(len(topk_json_path_list)):
        shape = topk_shape_list[index]
        json_path = topk_json_path_list[index]
        data = topk_json_data_list[index]
        if not json_path in json_path_shape_dic:
            json_path_shape_dic[json_path] = [shape]
            json_path_data_dic[json_path] = data
        else:
            json_path_shape_dic[json_path].append(shape)
    for json_path in json_path_shape_dic:
        shapes = json_path_shape_dic[json_path]
        json_data = json_path_data_dic[json_path]
        json_data['shapes'] = shapes
        json.dump(json_data, open(os.path.join(gs_topk_path, json_path), 'w', encoding='utf-8'), indent=4)
def args_para():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--jsons_dir", default='/home/lijq/Desktop/data/byd/workspace/byd_ipad_workspace/train_val_data/test/IPAD-12/segjson',type=str)
    parser.add_argument("--top_k", default=0.3,type=float)
    parser.add_argument("--gs_topk_path",default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/byd_ipad_workspace/train_val_data/test/IPAD-12' ,type=str)
    parser.add_argument("--gs_no_topk_path",type=str)
    parser.add_argument("--copy_flag",type=bool,default=True)
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args=args_para()
    sum=counter_cate(args.jsons_dir)
    print('sum____:',sum)
    topk=sum*args.top_k
    get_topk_guosha(gs_path=args.jsons_dir, topk=topk, gs_topk_path=args.gs_topk_path)
    print('after:',counter_cate(args.gs_topk_path))
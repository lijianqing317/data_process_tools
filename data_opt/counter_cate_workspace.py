import json
import glob
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic

def counter_cate(json_path,index_id):
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

    sum = 0
    for i in classes_dic:
        sum += classes_dic[i]
    print(classes_dic)
    dic_ = {}
    for i in list(classes_dic.keys()):
        dic_[i] = str(i).split('-')[0]
    print(dic_)
    with open(filename_txt, "a") as file:
        file.write('{}_文件夹：{}'.format(index_id,json_path))
        file.write('\r\n')
        file.write('缺陷名排序:{}'.format(sorted(list(classes_dic.keys()))))
        file.write('\r\n')
        file.write('缺陷数量排序:{}'.format(counter_sort))
        file.write('\r\n')
        file.write('缺陷种类:{}'.format(len(counter_sort)))
        file.write('\r\n')
        file.write('目标汇总数:{}'.format(sum))
        file.write('\r\n')
        file.write('类别字典:{}'.format(dic_))
        file.write('\r\n')
    return sum


def args_para():
    import argparse
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--workspace_dir", type=str,
                        default='/home/lijq/Desktop/data/O_ALL/workspace_single_crop')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    import os


    args=args_para()
    workspace_dir=args.workspace_dir
    filename_txt=os.path.join(workspace_dir,'all_static_nums_cls.txt')
    # 打开文件，并写入内容
    index_id=0
    for data_crop_name in os.listdir(workspace_dir):
        data_crop_path= os.path.join(workspace_dir,data_crop_name)
        for train_val_name in os.listdir(data_crop_path):
            train_val_path=os.path.join(data_crop_path,train_val_name)
            for batch_name in os.listdir(train_val_path):
                batch_path=os.path.join(train_val_path,batch_name)
                index_id+=1
                sum=counter_cate(batch_path,index_id)







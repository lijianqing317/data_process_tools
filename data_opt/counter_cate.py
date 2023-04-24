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
        dic_[i] = '{}'.format(str(i).split('-')[0])
        # dic_[i] = '{}-QX-S3'.format(str(i).split('-')[0])
    print(dic_)
    return sum


def args_para():
    import argparse
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--jsons_dir", type=str,
                        default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/all_new/data/image_mh')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args=args_para()
    sum=counter_cate(args.jsons_dir)
    '''
    缺陷名排序 ['aotu', 'huashang', 'overkill', 'pengshang', 'yashang']
缺陷数量排序 [('overkill', 413150), ('yashang', 1372), ('huashang', 961), ('pengshang', 811), ('aotu', 230)]
缺陷种类 5
目标汇总数： 416524
{'overkill': 413150, 'pengshang': 811, 'aotu': 230, 'yashang': 1372, 'huashang': 961}
{'overkill': 'overkill', 'pengshang': 'pengshang', 'aotu': 'aotu', 'yashang': 'yashang', 'huashang': 'huashang'}
    '''
    '''
    yuantu:
    缺陷数量排序 [('yise', 1454), ('heidian', 1432), ('pengshang', 1373), ('guashang', 1114), ('daowen', 770), ('yashang', 561), ('aotuhen', 524), ('tabian', 294), ('shahenyin', 226), ('shuahen', 195), ('lvjixian', 160), ('cashang', 150), ('liangdian', 134), ('maobian', 95), ('damohen', 76), ('zangwu', 71), ('duoliao', 28), ('bianxing', 26), ('guoqie', 12), ('yinglihen', 6)]
缺陷种类 20
目标汇总数： 8701
    miss
    缺陷数量排序 [ ('yise', 69),('heidian', 495), ('guashang', 79), ('pengshang', 74), ('aotuhen', 61), ('tabian', 27), ('daowen', 27), ('yashang', 21), ('liangdian', 16), ('maobian', 13), ('damohen', 9), ('shuahen', 7), ('cashang', 6), ('zangwu', 5), ('bianxing', 4), ('shahenyin', 4), ('lvjixian', 3), ('duoliao', 1), ('guoqie', 1)]
缺陷种类 19
目标汇总数： 922
    
    no_miss
    缺陷数量排序 [('yise', 1403), ('heidian', 1400), ('pengshang', 1324), ('guashang', 1085), ('daowen', 747), ('yashang', 559), ('aotuhen', 478), ('tabian', 268), ('shahenyin', 223), ('shuahen', 188), ('lvjixian', 157), ('cashang', 147), ('liangdian', 134), ('maobian', 82), ('damohen', 67), ('zangwu', 66), ('duoliao', 28), ('bianxing', 22), ('guoqie', 11), ('yinglihen', 6)]
缺陷种类 20
目标汇总数： 8395

    '''






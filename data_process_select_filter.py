"""
 @author  lijianqing
 @date  2022/12/6 下午10:54
 @version 1.0
"""
import argparse
import glob
import json
import os


def parse_para(input_json):
    with open(input_json, "r", encoding="utf-8") as f:
        ret_dic = json.load(f)
    return ret_dic


def save_json(dic, save_path):
    json.dump(dic, open(save_path, "w", encoding="utf-8"), indent=4)


def counter_cate(json_path):
    jsons = glob.glob("{}/*.json".format(json_path))
    classes_dic = {}
    for i in jsons:
        ret_dic = parse_para(i)
        shapes = ret_dic["shapes"]
        for j in shapes:
            if j["label"] not in classes_dic:
                classes_dic[j["label"]] = 1
            else:
                classes_dic[j["label"]] += 1
    counter_sort = sorted(classes_dic.items(), key=lambda x: x[1], reverse=True)
    print("缺陷名排序", sorted(list(classes_dic.keys())))
    print("缺陷数量排序", counter_sort)
    print("缺陷种类", len(counter_sort))
    sum = 0
    for i in classes_dic:
        sum += classes_dic[i]
    print("目标汇总数：", sum)


def generate_clean_json(
    modify_labelname={}, json_data={}, remove_image_data=True, filter=True
):
    shapes = json_data["shapes"]
    if remove_image_data:
        json_data["imageData"] = None

    if modify_labelname:
        try:
            new_shapes = []
            for shape in shapes:
                shape['flags']={}
                label = shape["label"]
                if label in modify_labelname:
                    shape["label"] = modify_labelname[label]
                    new_shapes.append(shape)
            if filter:
                json_data["shapes"] = new_shapes
            else:
                json_data["shapes"] = shapes

        except Exception as e:
            print("modify and filter class name except:{}".format(e))
    return json_data, len(new_shapes)


def process_modify_filter_class_dir(
    jsons_path="",
    jsons_save_path="",
    save_none_shapes=False,
    modify_labelname={},
    remove_image_data=True,
    filter=True,
):
    try:
        jsons_path_list = glob.glob("{}/*.json".format(jsons_path))
        if not os.path.exists(jsons_save_path):
            os.makedirs(jsons_save_path)
        for json_path in jsons_path_list:
            json_data = parse_para(json_path)
            clean_json_data, shapes_len = generate_clean_json(
                modify_labelname=modify_labelname,
                json_data=json_data,
                remove_image_data=remove_image_data,
                filter=filter,
            )
            if save_none_shapes:
                save_json(
                    clean_json_data, json_path.replace(jsons_path, jsons_save_path)
                )
            else:
                if shapes_len:
                    save_json(
                        clean_json_data, json_path.replace(jsons_path, jsons_save_path)
                    )
    except Exception as e:
        print("process_modify_filter_class_dir:{}".format(e))


if __name__ == "__main__":
    modify_labelname ={'guashang': 'guashang', 'duoliao': 'duoliao', 'aotuhen': 'aotuhen', 'pengshang': 'pengshang', 'penshabujun': 'yise',
                       'yashang': 'yashang', 'shahenyin': 'shahenyin', 'tabian': 'tabian', 'cashang': 'cashang', 'canjiao': 'yise', 'yise': 'yise',
                       'daowen': 'daowen', 'yinglihen': 'yinglihen', 'heidian': 'heidian', 'shuahen': 'shuahen', 'baidian': 'baidian'}
    modify_labelname={'pengshang': 'pengshang', 'heidian': 'heidian', 'guashang': 'guashang', 'duoliao': 'duoliao', 'maobian': 'maobian', 'yise': 'yise', 'aotuhen': 'aotuhen', 'tabian': 'tabian', 'daowen': 'daowen', 'shuahen': 'shuahen', 'cashang': 'cashang', 'lvjixian': 'lvjixian', 'bianxing': 'bianxing', 'liangdian': 'liangdian', 'damohen': 'damohen', 'yashang': 'yashang', 'shahenyin': 'shahenyin', 'fushi': 'fushi', '1': '1', 'guoqie': 'guoqie', 'zangwu': 'zangwu'}
    #{'guashang-QX-S3': 'guashang', 'yise-QX-S3': 'yise', 'yashang-QX-S3': 'yashang', 'pengshang-QX-S3': 'pengshang', 'shahenyin-QX-S3': 'shahenyin', 'aotuhen-QX-S3': 'aotuhen', 'daowen-QX-S3': 'daowen', 'daowen': 'daowen', 'tabian-QX-S3': 'tabian', 'cashang-QX-S3': 'cashang', 'shuahen-QX-S3': 'shuahen', 'canjiao-QX-S3': 'canjiao', 'guashang-QX-S4': 'guashang'}
    #modify_labelname={'aotu':'oneobj','yinglihen': 'oneobj', 'guashang': 'oneobj', 'aotuhen': 'oneobj', 'yise': 'oneobj', 'daowen': 'oneobj', 'heidian': 'oneobj', 'shuahen': 'oneobj', 'yashang': 'oneobj', 'liangdian': 'oneobj', 'guoqie': 'oneobj', 'tabian': 'oneobj', 'pengshang': 'oneobj', 'bianxing': 'oneobj'}
    #modify_labelname={'aotu':'oneobj','yinglihen': 'oneobj', 'guashang': 'oneobj', 'aotuhen': 'oneobj', 'yise': 'oneobj', 'daowen': 'oneobj', 'heidian': 'oneobj', 'shuahen': 'oneobj', 'yashang': 'oneobj', 'liangdian': 'oneobj', 'guoqie': 'oneobj', 'tabian': 'oneobj', 'pengshang': 'oneobj', 'bianxing': 'oneobj'}
    modify_labelname={'pengshang_ok': 'pengshang','heidian_ok': 'heidian', 'guashang_ok': 'guashang',  'cashang_ok': 'cashang', 'fushi_ok': 'fushi',  'yise_ok': 'yise',
                      'aotuhen_ok': 'aotuhen','daowen_ok': 'daowen', 'tabian_ok': 'tabian', 'yashang_ok': 'yashang', 'liangdian_ok': 'liangdian',
                      'shahenyin_ok': 'shahenyin', 'damohen_ok': 'damohen', 'yashang_Ok': 'yashang'}
    # modify_labelname = {'加铣': '加铣'}
    modify_labelname={'yashang': 'yashang', 'pengshang': 'pengshang', 'tabian': 'tabian', 'daowen': 'daowen', 'shahenyin': 'shahenyin', 'liangdian': 'liangdian', 'guashang': 'guashang', 'maobian': 'maobian'}
    modify_labelname={'yise': 'yise', 'yashang': 'yashang', 'pengshang': 'pengshang', 'daowen': 'daowen', 'aotuhen': 'aotuhen', 'guashang': 'guashang', 'shuahen': 'shuahen', 'shahenyin': 'shahenyin', 'lvjixian': 'lvjixian', 'cashang': 'cashang', 'heidian': 'heidian', 'tabian': 'tabian', 'liangdian': 'liangdian', 'duoliao': 'duoliao', 'fushi': 'fushi', 'damohen': 'damohen', 'guoqie': 'guoqie', 'maobian': 'maobian', 'bianxing': 'bianxing', 'yinglihen': 'yinglihen'}
    modify_labelname={'yise': 'yise', 'yashang': 'yashang', 'pengshang': 'pengshang', 'daowen': 'daowen', 'aotuhen': 'aotuhen', 'guashang': 'guashang', 'shuahen': 'shuahen', 'shahenyin': 'shahenyin', 'lvjixian': 'lvjixian', 'cashang': 'cashang', 'heidian': 'heidian', 'tabian': 'tabian', 'liangdian': 'liangdian', 'duoliao': 'duoliao', 'fushi': 'fushi', 'damohen': 'damohen', 'guoqie': 'guoqie', 'maobian': 'maobian', 'bianxing': 'bianxing', 'yinglihen': 'yinglihen'}
    modify_labelname={'pengshang-QX-S3': 'pengshang', 'yise-QX-S3': 'yise', 'guashang-QX-S3': 'guashang', 'liangdian-QX-S3': 'liangdian',
                      'aotuhen-QX-S3': 'aotuhen', 'shuahen-QX-S3': 'shuahen', 'heidian-QX-S3': 'heidian', 'daowen-QX-S3': 'daowen',
                      'tabian-QX-S3': 'tabian', 'yashang-QX-S3': 'yashang',
                     'damohen-QX-S3': 'damohen','shahenyin-QX-S3': 'shahenyin', 'cashang-QX-S3': 'cashang'}
    modify_labelname={'daowen': 'daowen', 'aotuhen': 'aotuhen', 'heidian': 'heidian', 'pengshang': 'pengshang', 'yise': 'yise', 'guashang': 'guashang', 'yashang': 'yashang', 'damohen': 'damohen', 'liangdian': 'liangdian', 'shahenyin': 'shahenyin', 'shuahen': 'shuahen', 'maobian': 'maobian', 'tabian': 'tabian', 'cashang': 'cashang', 'lvjixian': 'lvjixian', 'duoliao': 'duoliao', 'bianxing': 'bianxing', 'fushi': 'fushi', 'guoqie': 'guoqie'}
    modify_labelname={'daowen': 'daowen-QX-S3', 'aotuhen': 'aotuhen-QX-S3', 'heidian': 'heidian-QX-S3', 'pengshang': 'pengshang-QX-S3', 'yise': 'yise-QX-S3', 'guashang': 'guashang-QX-S3', 'yashang': 'yashang-QX-S3', 'damohen': 'damohen-QX-S3', 'liangdian': 'liangdian-QX-S3', 'shahenyin': 'shahenyin-QX-S3', 'shuahen': 'shuahen-QX-S3', 'maobian': 'maobian-QX-S3', 'tabian': 'tabian-QX-S3', 'cashang': 'cashang-QX-S3', 'lvjixian': 'lvjixian-QX-S3', 'duoliao': 'duoliao-QX-S3', 'bianxing': 'bianxing-QX-S3', 'fushi': 'fushi-QX-S3', 'guoqie': 'guoqie-QX-S3'}
    modify_labelname={'daowen': 'daowen-QX-S3', 'yise': 'yise-QX-S3', 'shuahen': 'shuahen-QX-S3', 'aotuhen': 'aotuhen-QX-S3', 'guashang': 'guashang-QX-S3', 'pengshang': 'pengshang-QX-S3', 'heidian': 'heidian-QX-S3', 'yashang': 'yashang-QX-S3', 'tabian': 'tabian-QX-S3', 'lvjixian': 'lvjixian-QX-S3', 'liangdian': 'liangdian-QX-S3', 'maobian': 'maobian-QX-S3', 'fushi': 'fushi-QX-S3', 'shahenyin': 'shahenyin-QX-S3', 'canjiao': 'canjiao-QX-S3'}
    modify_labelname={'daowen': 'daowen-QX-S3', 'yise': 'yise-QX-S3', 'heidian': 'heidian-QX-S3', 'pengshang': 'pengshang-QX-S3', 'damohen': 'damohen-QX-S3', 'guashang': 'guashang-QX-S3', 'overkill': 'overkill-QX-S3', 'yashang': 'yashang-QX-S3', 'aotuhen': 'aotuhen-QX-S3', 'maobian': 'maobian-QX-S3', 'tabian': 'tabian-QX-S3', 'liangdian': 'liangdian-QX-S3', 'shahenyin': 'shahenyin-QX-S3', 'lvjixian': 'lvjixian-QX-S3', 'shuahen': 'shuahen-QX-S3', 'fushi': 'fushi-QX-S3', 'cashang': 'cashang-QX-S3', 'bianxing': 'bianxing-QX-S3', 'guoqie': 'guoqie-QX-S3'}
    modify_labelname={'liangdian-QX-S3':'liangdian-QX-S3'}
    modify_labelname={'liangdian':'liangdian'}
    modify_labelname={'pengshang-mian': 'pengshang', 'yashang': 'yashang', 'guashang-baiduan': 'guashang', 'yise-hei': 'yise', 'daowen-mian': 'daowen', 'yise-heitiao': 'yise', 'heidian': 'heidian', 'guashang-heiduan': 'guashang', 'shahenyin': 'shahenyin', 'guashang-heibai': 'guashang', 'pengshang-bian': 'pengshang', 'duoliao': 'duoliao', 'yinglihen': 'yinglihen', 'guashang-heizhang': 'guashang', 'baidian': 'baidian', 'penshabujun-hei': 'penshabujun', 'maoxu': 'maoxu', 'yise-baitiao': 'yise', 'tubao': 'aotuhen', 'aohen': 'aotuhen', 'yise-bai': 'yise', 'yise-hui': 'yise', 'guashang-baizhang': 'guashang', 'tabian-liang': 'tabian', 'yiwu': 'yiwu', 'daowen-dantiao': 'daowen', 'mianhua': 'mianhua', 'pengshang-zhang': 'pengshang', 'tabian-an': 'tabian', 'penshabujun-bai': 'penshabujun', 'aotuhen2': 'aotuhen', 'bianxing': 'bianxing', 'pengshang-jiao': 'pengshang', 'daowen-jiao': 'daowen'}
    modify_labelname={'pengshang-mian': 'pengshang', 'yashang': 'yashang', 'guashang-baiduan': 'guashang', 'yise-hei': 'yise', 'daowen-mian': 'daowen', 'yise-heitiao': 'yise', 'heidian': 'heidian', 'guashang-heiduan': 'guashang', 'shahenyin': 'shahenyin', 'guashang-heibai': 'guashang', 'pengshang-bian': 'pengshang', 'duoliao': 'duoliao', 'yinglihen': 'yinglihen', 'guashang-heizhang': 'guashang', 'baidian': 'baidian', 'penshabujun-hei': 'penshabujun', 'maoxu': 'maoxu', 'yise-baitiao': 'yise', 'tubao-kuai': 'aotuhen', 'aohen-kuai': 'aotuhen', 'yise-bai': 'yise', 'yise-hui': 'yise', 'guashang-baizhang': 'guashang', 'tabian-liang': 'tabian', 'yiwu': 'yiwu', 'daowen-dantiao': 'daowen', 'mianhua': 'mianhua', 'pengshang-zhang': 'pengshang', 'tabian-an': 'tabian', 'penshabujun-bai': 'penshabujun', 'aotuhen2': 'aotuhen', 'bianxing': 'bianxing', 'pengshang-jiao': 'pengshang', 'daowen-jiao': 'daowen'}
    modify_labelname={'pengshang-QX-S4': 'pengshang', 'yashang-QX-S3': 'yashang', 'pengshang-QX-S3': 'pengshang', 'yashang-QX-S4': 'yashang', 'huashang-QX-S4': 'huashang',
                      'huashang-QX-S3': 'huashang', 'aotu-QX-S3': 'aotu', 'pengshang': 'pengshang', 'pengshang-QX-S2': 'pengshang'}
    modify_labelname={'pengshang-MH-S3':'pengshang'}
    jsons_path = "/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/all_new/data/image"
    save_jsons_path = "/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/all_new/data/image_mh"
    remove_image_data = True
    save_none_shapes = False
    filter = True
    counter_classes = True
    parser = argparse.ArgumentParser(description="modify name and filter class")
    parser.add_argument(
        "--jsons_path", type=str, default=jsons_path, help="path for jsons"
    )
    parser.add_argument(
        "--save_jsons_dir",
        type=str,
        default=save_jsons_path,
        help="path for save jsons",
    )
    parser.add_argument(
        "--remove_image_data",
        type=bool,
        default=remove_image_data,
        help="remove imagedata in json",
    )
    parser.add_argument(
        "--save_none_shapes",
        type=bool,
        default=save_none_shapes,
        help="save none shapes?",
    )
    parser.add_argument(
        "--modify_labelname", type=dict, default=modify_labelname, help="filter labels"
    )
    parser.add_argument("--filter", type=bool, default=filter, help="filter labels")
    parser.add_argument(
        "--counter_classes", type=bool, default=counter_classes, help="counter_classes"
    )

    args = parser.parse_args()
    print("------------------正在处理-----------------")
    process_modify_filter_class_dir(
        jsons_path=args.jsons_path,
        jsons_save_path=args.save_jsons_dir,
        save_none_shapes=save_none_shapes,
        modify_labelname=args.modify_labelname,
        remove_image_data=args.remove_image_data,
        filter=args.filter,
    )
    print("------------------处理完毕-----------------")
    if args.counter_classes:
        print("---------------数据处理前统计----------")
        counter_cate(args.jsons_path)
        print("---------------数据处理后统计----------")
        counter_cate(args.save_jsons_dir)

import os
import shutil
import argparse
def select_same_name_file(template_path,templateformat,soure_path,target_path,targetformat=[],operate_copy_or_move_flag = True):
    for file_name in os.listdir(template_path):
        print('targetformat', targetformat)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        for i in targetformat:
            try:
                target_name = file_name.replace(templateformat,i)
                print('target_name', target_name)
                if operate_copy_or_move_flag:
                    shutil.copy(os.path.join(soure_path,target_name),os.path.join(target_path,target_name))
                else:
                    shutil.move(os.path.join(soure_path,target_name),os.path.join(target_path,target_name))
            except:
                continue

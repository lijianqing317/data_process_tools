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

import os
import shutil
import argparse


def select_same_name_file(template_path, templateformat, soure_path, target_path, targetformat=[],
                          operate_copy_or_move_flag=True):
    for file_name in os.listdir(template_path):
        print('targetformat', targetformat)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        for i in targetformat:
            try:
                target_name = file_name.replace(templateformat, i)
                print('target_name', target_name)
                if operate_copy_or_move_flag:
                    shutil.copy(os.path.join(soure_path, target_name), os.path.join(target_path, target_name))
                else:
                    shutil.move(os.path.join(soure_path, target_name), os.path.join(target_path, target_name))
            except:
                continue


if __name__ == "__main__":
    modify_labelname = {'pengshang-QX-S4': 'pengshang', 'yashang-QX-S3': 'yashang', 'pengshang-QX-S3': 'pengshang',
                        'yashang-QX-S4': 'yashang', 'huashang-QX-S4': 'huashang',
                        'huashang-QX-S3': 'huashang', 'aotu-QX-S3': 'aotu', 'pengshang': 'pengshang',
                        'pengshang-QX-S2': 'pengshang','pengshang-MH-S3': 'pengshang'}
    jsons_path = "/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/all_new/data/image"
    save_jsons_path = "/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/all_new/data/image_ALL"
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

    select_same_name_file(save_jsons_path, 'json', jsons_path, save_jsons_path,
                          targetformat=['jpg'], operate_copy_or_move_flag=True)




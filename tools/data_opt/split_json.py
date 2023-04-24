'''
 @author  lijianqing
 @date  2023/2/9 下午2:21
 @version 1.0
'''
import json
def parse_para(input_json):
    with open(input_json, "r", encoding="utf-8") as f:
        ret_dic = json.load(f)
    return ret_dic


def save_json(dic, save_path):
    json.dump(dic, open(save_path, "w", encoding="utf-8"), indent=4)


path_merge_json='/home/lijq/Desktop/data/O_ALL/overkill/liangchanji/overkill.json'

def get_dic(json_data):
    jsons_dic={}
    for key in json_data['RECORDS'][0]:
        print('key---',key)
    for shape in json_data['RECORDS']:
        task_name=shape['TaskID']
        workpiece_name=shape['WorkpieceID']
        picture_name=shape['PictureID']
        json_name='{}-{}-{}.json'.format(str(task_name).zfill(4),str(workpiece_name).zfill(4),picture_name)
        if not json_name in jsons_dic:
            jsons_dic[json_name]=[]
        else:
            jsons_dic[json_name].append(shape)

    return jsons_dic

def main():
    json_data=parse_para(path_merge_json)
    jsons_dic=get_dic(json_data)
    print('len',len(jsons_dic))
    print(json_data['RECORDS'][0])
    print(jsons_dic.keys())

if __name__ == '__main__':
    main()

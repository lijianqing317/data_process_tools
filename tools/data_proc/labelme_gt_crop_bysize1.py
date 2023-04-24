'''
 @author  lijianqing
 @date  2023/1/10 上午11:22
 @version 1.0
'''
import argparse
import glob
# author
import json
import math
import multiprocessing
import os
import time

import cv2

'''
@CutLabelme: 根据给定size(w,h)和标注切图
            主要功能：将mark工具标注的xml标注转为json标注，方便labelme查看及生成coco格式数据
            关键处理：1.将全图标注数据根据给定size计算终止切图策略，由digui函数实现；
                    2.切图策略计算过程中，记录最新框的中心位置；
                    3.计算切图的大小和对应新json中坐标位置；
                    4.超出边界的目标切落在区域内的。
@author: lijianqing
@date: 2020/11/24 16:45
@return 
'''


class CutLabelme(object):
    def __init__(self, labelme_dir, save_dir, crop_size_w, crop_size_h, process_nums, padding, line_width):
        self.cut_w = crop_size_w
        self.cut_h = crop_size_h
        self.img_jsons = labelme_dir
        self.process_nums = process_nums
        self.out_path_result_cut = save_dir
        self.padding = padding
        self.line_width = line_width
        self.main()

    def save_json(self, dic, save_path):
        json.dump(dic, open(save_path, 'w', encoding='utf-8'), indent=4)

    def circle_2_polygon(self, center_points, r, r_nums=10):
        new_points_1 = []
        new_points_2 = []
        new_points_3 = []
        new_points_4 = []
        r_ = r / r_nums
        center_points_x, center_points_y = center_points

        for i in range(r_nums):
            # print(r_, r_nums, "-----", i)
            w = i * r_
            h = math.sqrt(r ** 2 - w ** 2)
            # print("w,h,r", w, h, r)
            new_points_1.append([center_points_x - w, center_points_y - h])
            new_points_2.append([center_points_x - w, center_points_y + h])
            new_points_3.append([center_points_x + w, center_points_y + h])
            new_points_4.append([center_points_x + w, center_points_y - h])
            if i == r_nums - 1:
                new_points_1.append([center_points_x - r, center_points_y])
                new_points_3.append([center_points_x + r, center_points_y])
                # new_points_4.append([center_points_x + w, center_points_y - h])

        new_points = []
        new_points.extend(new_points_1)
        new_points.extend(list(reversed(new_points_2)))
        new_points.extend(new_points_3)
        new_points.extend(list(reversed(new_points_4)))
        return new_points

    def trans_shape_points(self, shape):
        shape_type = shape["shape_type"]
        points = shape["points"]
        new_points = []
        if shape_type == "point":
            shape_type = "circle"
            point_0 = points[0]
            r = 2
            x, y = point_0
            point_1 = [x + r, y]
            new_points_ = []
            new_points_.append(point_0)
            new_points_.append(point_1)
            shape["points"] = new_points_
            shape["shape_type"] = shape_type
            points = new_points_
        if shape_type == "circle":  # to 12 points
            center_points_x, center_points_y = points[0]
            edage_points_x, edage_points_y = points[1]
            r = math.sqrt(
                (center_points_x - edage_points_x) ** 2
                + (center_points_y - edage_points_y) ** 2
            )
            new_points = self.circle_2_polygon(points[0], r)
            new_shape_type = "polygon"
            print("shape_type", shape_type)
            print("points", points)
            print("new_points", new_points)
        elif shape_type == "line":
            first_points_x, first_points_y = points[0]
            second_points_x, second_points_y = points[1]
            r = 2
            if (
                    abs(first_points_x - second_points_x) < 1
                    and abs(first_points_y - second_points_y) >= 1
            ):
                new_points.append([first_points_x - r, first_points_y])
                new_points.append([first_points_x + r, first_points_y])
                new_points.append([second_points_x + r, second_points_y])
                new_points.append([second_points_x - r, second_points_y])
                new_shape_type = "polygon"
            elif (
                    abs(first_points_x - second_points_x) >= 1
                    and abs(first_points_y - second_points_y) < 1
            ):
                new_points.append([first_points_x, first_points_y - r])
                new_points.append([first_points_x, first_points_y + r])
                new_points.append([second_points_x, second_points_y + r])
                new_points.append([second_points_x, second_points_y - r])
                new_shape_type = "polygon"
            elif (
                    abs(first_points_x - second_points_x) < 1
                    and abs(first_points_y - second_points_y) < 1
            ):
                new_points.append([first_points_x - r, first_points_y - r])
                new_points.append([second_points_x - r, second_points_y - r])
                new_points.append([first_points_x + r, first_points_y + r])
                new_points.append([second_points_x + r, second_points_y + r])
                new_shape_type = "polygon"
            else:
                new_points = points
                new_shape_type = shape_type
            # print('new_shape_type:',new_shape_type)
        else:
            new_points = points
            new_shape_type = shape_type
        shape["points"] = new_points
        shape["shape_type"] = new_shape_type
        # print('shape:flags', shape['flags'])
        shape["flags"] = {}
        # print('shape:flags1', shape['flags'])
        return shape

    def save_new_img(self, img_np, img_name, xmin, ymin, xmax, ymax, out_path, img_x, img_y):
        # 切图并保存
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        left, top, right, down = 0, 0, 0, 0  # need padding size
        if xmax > img_x:
            right = xmax - img_x
            xmax = img_x
            # print('out of width')
        if ymax > img_y:
            down = ymax - img_y
            ymax = img_y
            # print('out of hight')
        if ymin < 0:
            top = abs(ymin)
            ymin = 0
            # print('out of hight')
        if xmin < 0:
            left = abs(xmin)
            xmin = 0
            # # print('out of width')
        img_crop = img_np[ymin:ymax, xmin:xmax]
        ret = cv2.copyMakeBorder(img_crop, top, down, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))  # padding
        cv2.imwrite(os.path.join(out_path, img_name), ret)
        return 0

    def count_bbox_size(self, per_object):
        points = per_object['points']
        x, y = zip(*points)  # split x,y
        if per_object['shape_type'] == 'circle':
            center_point = points[0]
            r_p = points[1]
            r = round(math.sqrt((center_point[0] - r_p[0]) ** 2 + (center_point[1] - r_p[1]) ** 2), 2)
            min_x = round(center_point[0] - r, 2)
            min_y = round(center_point[1] - r, 2)
            max_x = round(center_point[0] + r, 2)
            max_y = round(center_point[1] + r, 2)
        else:
            min_x = round(min(x), 2)
            min_y = round(min(y), 2)
            max_x = round(max(x), 2)
            max_y = round(max(y), 2)
        # print('max_x,max_y,min_x,min_y',max_x,max_y,min_x,min_y,'---',i['shape_type'])
        return max_x, max_y, min_x, min_y

    def get_new_location(self, point, mid_point, crop_w=64, crop_h=64):
        # 将缺陷放于中心位置
        p_x = point[0] - mid_point[0] + crop_w / 2
        p_y = point[1] - mid_point[1] + crop_h / 2
        if p_x < 0:
            p_x = 0
        if p_y < 0:
            p_y = 0
        if p_x > crop_w:
            p_x = crop_w
        if p_y > crop_h:
            p_y = crop_h
        return [p_x, p_y]

    def cut_json(self, json_p):
        print('jsons-----', json_p)
        counter_per_cut = 0
        with open(json_p, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        img_n = json_p.replace('json', 'jpg')
        if not os.path.exists(img_n):
            img_n = json_p.replace('json', 'png')
        # print('img_n 图像位置：',img_n)
        img_np = cv2.imread(img_n)  # 原图数据
        image_name_path = json_data['imagePath'].split('.')[0]
        # print('img_np----图像数据',img_np)
        shapes_img_l = {}
        c = 0
        # 筛选需要切的label
        for i in json_data['shapes']:
            c += 1
            trans_shape = self.trans_shape_points(i)
            shapes_img_l[c] = trans_shape
        cut_one_img = []
        mid_point = []
        self.recursion_cut(shapes_img_l, counter_per_cut, self.cut_w, self.cut_h, cut_one_img, mid_point)  # 聚类
        for index_object in range(len(cut_one_img)):
            for shapes_object in cut_one_img[index_object]:
                new_points = []
                for loc in shapes_object['points']:
                    n_p = self.get_new_location(loc, mid_point[index_object], self.cut_w, self.cut_h)
                    new_points.append(n_p)
                shapes_object['points'] = new_points

            new_name_img = '{}_{}_{}_{}.jpg'.format(mid_point[index_object][0], mid_point[index_object][1],
                                                    index_object, image_name_path)
            new_name_json = '{}_{}_{}_{}.json'.format(mid_point[index_object][0], mid_point[index_object][1],
                                                      index_object, image_name_path)
            # 生成新的img文件，抠图过程中会出现超出边界的坐标
            source_x_min, source_x_max = mid_point[index_object][0] - self.cut_w / 2, mid_point[index_object][
                0] + self.cut_w / 2  # 抠图位置
            source_y_min, source_y_max = mid_point[index_object][1] - self.cut_h / 2, mid_point[index_object][
                1] + self.cut_h / 2
            x_min, x_max, y_min, y_max = int(source_x_min), int(source_x_max), int(source_y_min), int(source_y_max)
            self.save_new_img(img_np, new_name_img, x_min, y_min, x_max, y_max, self.out_path_result_cut,
                              json_data['imageWidth'], json_data['imageHeight'])
            # 生成新的json文件
            # crop_szie_w,crop_szie_h = crop_szie,crop_szie
            self.def_new_json(json_data, self.cut_w, self.cut_h, new_name_json, cut_one_img[index_object],
                              self.out_path_result_cut, new_name_img)

    def def_new_json(self, json_data, crop_szie_w, crop_size_h, new_name, shapes_img, out_p, new_name_img):
        new_json = {}
        new_json['flags'] = ''  # json_data['flags']
        new_json['imageData'] = None
        try:
            new_json['imageDepth'] = json_data['imageDepth']
        except:
            new_json['imageDepth'] = 3
        new_json['imageHeight'] = crop_size_h
        new_json['imageLabeled'] = ''  # json_data['imageLabeled']
        new_json['imagePath'] = new_name_img
        new_json['imageWidth'] = crop_szie_w
        new_json['shapes'] = shapes_img
        new_json['time_Labeled'] = ''  # json_data['time_Labeled']
        new_json['imagePathSource'] = json_data['imagePath']
        new_json['version'] = json_data['version']
        self.save_json(new_json, os.path.join(out_p, new_name))
        # print('生成了',os.path.join(out_p,new_name))
        return new_json

    def def_dic_element(self, shapes_img, i, points):
        dic_element = {}
        dic_element['flags'] = i['flags']
        dic_element['group_id'] = i['group_id']
        dic_element['label'] = i['label']
        dic_element['points'] = points
        dic_element['shape_type'] = i['shape_type']
        dic_element['width'] = i['width']
        dic_element['flags'] = {}
        shapes_img.append(dic_element)
        return shapes_img

    def recursion_cut(self, shapes_img_l, counter_per_cut, crop_w, crop_h, cut_one_img, mid_point):
        counter_per_cut += 1
        if len(shapes_img_l) == 0:
            # print('递归结束了',counter_per_cut)
            return 0
        next_allow = {}  # 记录不可以放一起的标注
        allow = []
        max_bbox = []
        for i in shapes_img_l:
            max_x, max_y, min_x, min_y = self.count_bbox_size(shapes_img_l[i])  # 获取标注的位置
            w, h = max_x - min_x, max_y - min_y
            # 与已有点比较距离
            if len(max_bbox) > 0:
                a, b, c, d = max_bbox
                mmin_x = min(min_x, c)
                mmin_y = min(min_y, d)
                mmax_x = max(max_x, a)
                mmax_y = max(max_y, b)
                ww, hh = mmax_x - mmin_x, mmax_y - mmin_y
                # print('最大长宽',ww,hh)
                if ww < crop_w and hh < crop_h:
                    max_bbox = mmax_x, mmax_y, mmin_x, mmin_y
                    allow.append(shapes_img_l[i])
                else:
                    next_allow[i] = shapes_img_l[i]  # 不可以放一起的
            else:
                max_bbox = [max_x, max_y, min_x, min_y]
                allow.append(shapes_img_l[i])

        # 计算聚类后类别在原图的中心点。
        w, h = max_bbox[0] - max_bbox[2], max_bbox[1] - max_bbox[3]
        mid_x = math.ceil(max_bbox[2] + w / 2)
        mid_y = math.ceil(max_bbox[3] + h / 2)
        # print('中心点',math.ceil(mid_x),math.ceil(mid_y))
        cut_one_img.append(allow)
        mid_point.append((mid_x, mid_y))
        self.recursion_cut(next_allow, counter_per_cut, crop_w, crop_h, cut_one_img, mid_point)

    def main(self):
        jsons_path_list = self.img_jsons
        if not os.path.exists(self.out_path_result_cut):
            os.makedirs(self.out_path_result_cut)
        pool1 = multiprocessing.Pool(processes=self.process_nums)
        start_time = time.time()
        pool1.map(self.cut_json, glob.glob('{}/*.json'.format(jsons_path_list)))
        print('cut_labelme_img run time:', time.time() - start_time)
        pool1.close()
        pool1.join()


def get_parser():
    parser = argparse.ArgumentParser(description='The tool used to preprocess the dataset before training.')
    parser.add_argument('--data_dir',
                        default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/workspace_0315/data_cropped/val/original_ipad',
                        type=str, help='', )
    parser.add_argument('--save_dir',
                        default='/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/byd/workspace/workspace_0315/data_cropped/val/original_ipad_data_cropped768',
                        type=str, help='', )
    parser.add_argument('--crop_size_w', default=225, type=str, help='', )
    parser.add_argument('--crop_size_h', default=225, type=str, help='', )
    parser.add_argument('--line_width', default=2, type=str, help='', )
    parser.add_argument('--padding', default=True, type=str, help='', )
    parser.add_argument('--process_nums', default=8, type=str, help='', )
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = get_parser()
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    else:
        print('oooo')

    CutLabelme(args.data_dir, args.save_dir, args.crop_size_w, args.crop_size_h, args.process_nums, args.padding,
               args.line_width)

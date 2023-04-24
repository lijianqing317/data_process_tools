"""
 @author  lijianqing
 @date  2022/12/30 下午5:59
 @version 1.0
"""
import argparse
import json
import os
import glob
import cv2
import numpy as np
import math


def get_new_location(points, min_x, min_y):
    new_points = []
    for point in points:
        x_p, y_p = point
        new_points.append([x_p - min_x + 1, y_p - min_y + 1])
    return new_points


def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def save_json(dic, save_path):
    json.dump(
        dic, open(save_path, "w", encoding="utf-8"), indent=4, default=default_dump
    )


def circle_2_polygon(center_points, r, r_nums=10):
    new_points_1 = []
    new_points_2 = []
    new_points_3 = []
    new_points_4 = []
    r_ = r / r_nums
    center_points_x, center_points_y = center_points

    for i in range(r_nums):
        print(r_, r_nums, "-----", i)
        w = i * r_
        h = math.sqrt(r ** 2 - w ** 2)
        print("w,h,r", w, h, r)
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


def trans_shape_points(shape):
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
        new_points = circle_2_polygon(points[0], r)
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
    return shape


def crop_dir(args):
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    image_format = args.img_ext
    for json_path in glob.glob("{}/*.json".format(args.labelme_dir)):
        image_path = json_path.replace("json", image_format)
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            img_np = cv2.imread(image_path)  # 原图数据
        name_index = 0
        imagePath = json_data["imagePath"]
        for shape_old in json_data["shapes"]:
            shape = trans_shape_points(shape_old)
            points = shape["points"]
            min_x, max_x = min(np.array(points)[:, 0]), max(np.array(points)[:, 0])
            min_y, max_y = min(np.array(points)[:, 1]), max(np.array(points)[:, 1])
            # print('min_x,min_y', min_x, min_y)
            # print('max_x,max_y', max_x, max_y)
            new_points = get_new_location(points, min_x, min_y)
            # print('new points', new_points)

            new_image = img_np[int(min_y) : int(max_y) + 3, int(min_x) : int(max_x) + 3]

            name_index += 1
            image_name = str(imagePath).split(".")[0]
            new_img_name = "{}_{}.{}".format(image_name, name_index, image_format)
            new_json_name = new_img_name.replace(image_format, "json")

            shape["points"] = new_points
            new_shape = shape
            json_data["imagePathSource"] = imagePath
            json_data["imagePath"] = new_img_name
            json_data["imageHeight"] = max_y - min_y
            json_data["imageWidth"] = max_x - min_x
            json_data["shapes"] = [new_shape]
            new_data_dic = json_data
            try:
                cv2.imwrite(os.path.join(args.save_dir, new_img_name), new_image)
                save_json(new_data_dic, os.path.join(args.save_dir, new_json_name))
                # print('x_min,y_min,x_max,y_max,w,h', min_x, min_y, max_x, max_y, max_x - min_x, max_y - min_y)
            except Exception as e:
                print(e)
                print("new_image:", new_image)
                print("shape_type", shape["shape_type"])
                print("shape_type_old", shape_old["shape_type"])
                print(
                    "x_min,y_min,x_max,y_max,w,h",
                    min_x,
                    min_y,
                    max_x,
                    max_y,
                    max_x - min_x,
                    max_y - min_y,
                )
                print("imagePath", imagePath)
                print("shape_points", shape["points"])
                print("shape_old_points", shape_old["points"])


def get_parser():
    parser = argparse.ArgumentParser(
        description="The tool used to preprocess the dataset before training."
    )
    parser.add_argument("--labelme-dir", required=True, type=str, help="")
    parser.add_argument("--save-dir", required=True, type=str, help="")
    parser.add_argument("--img-ext", type=str, default="jpg", help="")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_parser()
    try:
        crop_dir(args)
    except Exception as e:
        print(e)

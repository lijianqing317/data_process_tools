'''
 @author  lijianqing
 @date  2023/3/24 下午2:49
 @version 1.0
'''
import os
workspace_dir='/home/lijq/Desktop/data/O_ALL/workspace_single'
data_dir='data'
miss_dir='data_miss'
gt_data=os.path.join(workspace_dir,data_dir)
miss_data=os.path.join(workspace_dir,miss_dir)
for miss_data_file in 1:9
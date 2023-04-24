import os
import shutil

def split_channelId(source_path,out_p):
    for i in os.listdir(source_path):
        channel_id = i.split('.')[0].split('-')[-1]
        channel_path = os.path.join(out_p,channel_id)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)
        shutil.move(os.path.join(source_path,i),os.path.join(channel_path,i))
    # if os.path.isdir(source_path):
    #     shutil.rmtree(source_path)

def merge_channelId(source_path,out_p):
    for root, dirs, files in os.walk(source_path):
        if len(dirs)==0:
            for file in files:
                save_path = out_p
                file_path = os.path.join(root,file)
                save_file_path = os.path.join(save_path,file)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                shutil.move(file_path,save_file_path)
    # if os.path.isdir(source_path):
    #     shutil.rmtree(source_path)
source_path= r'/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/R/origin/images_'
out_p = r'/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/R/origin/images'
split_channelId(source_path,out_p)
#merge_channelId(source_path,out_p)


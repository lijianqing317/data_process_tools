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

def args_para1():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--template_path", type=str,default='/home/lijq/Desktop/data/byd/workspace/workspace_merge_overkill/train_val_data_cropped/train/original_ipad_merge_not_topk_overkill_jsons')
    parser.add_argument("--templateformat", type=str,default='json')
    parser.add_argument("--source_path", type=str,default='/home/lijq/Desktop/data/byd/workspace/workspace_merge_overkill/train_val_data_cropped/train/original_ipad_merge_not_topk_overkill')
    parser.add_argument("--target_path",type=str,default='/home/lijq/Desktop/data/byd/workspace/workspace_merge_overkill/train_val_data_cropped/train/original_ipad_merge_not_topk_overkill_jsons')
    parser.add_argument("--targetformat",default=['jpg'])
    parser.add_argument("--copy_flag",type=bool,default=True)
    args = parser.parse_args()
    return args
def args_para():
    parser = argparse.ArgumentParser(description="modify name and filter class")
    parser.add_argument("--workspace", type=str,default='/home/lijq/Desktop/data/O_ALL/workspace_single')
    parser.add_argument("--data", type=str,default='data')
    parser.add_argument("--data_select",type=str,default='data_miss')
    parser.add_argument("--data_no_select",type=str,default='data_GT_miss')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args=args_para()
    args = args_para()
    workspace = args.workspace
    data = os.path.join(workspace, args.data)
    data_select = os.path.join(workspace, args.data_select)
    data_no_select = os.path.join(workspace, args.data_no_select)
    for train_val_file in os.listdir(data_select):
        sub_train_val_file = os.path.join(data_select, train_val_file)
        for data_batch_name in os.listdir(sub_train_val_file):
            data_batch_file = os.path.join(sub_train_val_file, data_batch_name)
            input_overkill = data_batch_file.replace(data_select, data)
            input_overkill_top = data_batch_file
            input_overkill_no_top = data_batch_file.replace(data_select, data_no_select)
            template_path=input_overkill_top
            templateformat='json'
            source_path=input_overkill
            target_path=input_overkill_no_top
            select_same_name_file(template_path,'json',source_path,target_path,targetformat=['json','jpg'],operate_copy_or_move_flag = False)


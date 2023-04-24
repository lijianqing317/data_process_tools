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

def args_para():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--template_path", type=str,default='/home/lijq/Desktop/data/O_ALL/workspace_single/data_GT_miss_zl/train/O_ok')
    parser.add_argument("--templateformat", type=str,default='json')
    parser.add_argument("--source_path", type=str,default='/home/lijq/Desktop/data/O_ALL/workspace_single/data_GT_miss_zl/train/O')
    parser.add_argument("--target_path",type=str,default='/home/lijq/Desktop/data/O_ALL/workspace_single/data_GT_miss_zl/train/O_ok')
    parser.add_argument("--targetformat",default=['jpg'])
    parser.add_argument("--copy_flag",type=bool,default=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args=args_para()
    select_same_name_file(args.template_path,args.templateformat,args.source_path,args.target_path,targetformat=args.targetformat,operate_copy_or_move_flag = args.copy_flag)


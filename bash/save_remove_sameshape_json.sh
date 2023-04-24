OVERKILL_DIR=${1:-/home/lijq/Desktop/data/O_ALL/workspace_single/data_pre/O}
OVERKILL_TOPK_DIR=${2:-$OVERKILL_DIR}
NO_OVERKILL_TOPK_DIR=${3:-train_val_data_cropped}
CODE_DIR=${4:/home/lijq/Desktop/data/code/data_preocess_tools}
COPY_FLAG=${5:True}
# 裁图
PYTHONPATH=$(pwd):$PYTHONPATH \
python3 tools/data_opt/remove_samename_json_sameshape.py \
    --input_overkill $WORK_DIR \
    --input_overkill_top $DATA_DIR \
    --input_overkill_no_top $CROP_DIR




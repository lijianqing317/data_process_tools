WORK_DIR=${1:-/home/lijq/Desktop/data/O_ALL/workspace_single}
DATA_DIR=${2:-$WORK_DIR/data}
MISS_DIR=${3:-$WORK_DIR/data_miss}
NOMISS_DIR=${4:-$WORK_DIR/data_no_miss}
COPY_FLAG=${5:True}
CODE_DIR=${6:/home/lijq/Desktop/data/code/data_preocess_tools}
cd $CODE_DIR
#文具件不存在则新建
if [ ! -d $NOMISS_DIR ]; then
  mkdir $NOMISS_DIR
fi

for MISS_file in $MISS_DIR/*/*
do
  DATA_DIR_FILE=${MISS_file/$MISS_DIR/$DATA_DIR}
  NOMISS_DIR_FILE=${MISS_file/$MISS_DIR/$NOMISS_DIR}
  echo $DATA_DIR_FILE
  echo $NOMISS_DIR_FILE
  PYTHONPATH=$(pwd):$PYTHONPATH \
  python3 data_opt/remove_samename_json_sameshape.py \
    --input_overkill $DATA_DIR_FILE \
    --input_overkill_top $MISS_file \
    --input_overkill_no_top $NOMISS_DIR_FILE
  echo "The finished"
done







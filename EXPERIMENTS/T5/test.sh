RGPU=$1
DATASET=$2
MODEL=$3
ExNAME=$4


CUDA_VISIBLE_DEVICES=$RGPU python T5.py -d $DATASET -m $MODEL -e $ExNAME -t True
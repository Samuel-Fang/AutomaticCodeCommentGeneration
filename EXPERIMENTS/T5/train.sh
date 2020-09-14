function make_dir () {
    if [[ ! -d "$1" ]]; then
        mkdir $1
    fi
}

RGPU=$1
DATASET=$2
MODEL=$3
ExNAME=$4

make_dir results/$ExNAME

CUDA_VISIBLE_DEVICES=$RGPU python T5.py -d $DATASET -m $MODEL -e $ExNAME
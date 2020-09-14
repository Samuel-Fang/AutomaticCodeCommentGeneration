# Run in the current directory
#$ -cwd
# Import current environment
#$ -V
# Run for up to 6 hours
#$ -l h_rt=6:00:00
# Use up to 4.8Gbytes per core
#$ -l h_vmem=4.8G
# Use up to 10 cores
#$ -pe smp 10

# This is a sample job submission based on what I can gather you were
# trying to submit before.  I don't know this code can use multiple cores
# but given we're trying to find out how much RAM it needs and are asking
# for quite a lot, we may as well have them and find out

DATA_DIR=data/CSN
DESC=Ex6T2
SEED=239
CUDA=0

# I'm not sure what python environment you need to make this run

./train_python.sh $DATA_DIR $DESC $CUDA $SEED

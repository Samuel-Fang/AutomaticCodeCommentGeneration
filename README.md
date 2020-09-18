# AutomaticCodeCommentGeneration
Code for MSc Project of Yicheng Fang, University of Leeds.
## Play with T5-small pre-trained model for automatic code comment generation
This is the guide for a interactive demo of generating code comment on T5-small pre-trained model
### Requirements
python 3.6 or above  
torch 1.4 or above  
[transformers](https://github.com/huggingface/transformers)  
ntlk  
rouge   
  
The demo and the test need to be run on GPU.
### Clone this repository and go to the correspoinding directory
```
git clone https://github.com/Samuel-Fang/AutomaticCodeCommentGeneration
cd AutomaticCodeCommentGeneration/EXPERIMENTS/T5
```
### Download the trained model files
```
cd results/CSNpyEx2/model
wget https://leedsmscsamuelfang.s3.eu-west-2.amazonaws.com/checkpoint-34000.tar.gz
tar -zxvf checkpoint-34000.tar.gz
cd ../../..
```
### generate comment for corresponding code on T5-small pre-trained model (Run the interactive demo)
```
python T5Generate.py
```

### test the T5-small pre-trained model on test dataset (Run the test)
```
./test.sh 0,1 CSNpython T5-small CSNpyEx2
```

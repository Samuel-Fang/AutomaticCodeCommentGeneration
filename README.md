# AutomaticCodeCommentGeneration
Code for MSc Project of Yicheng Fang, University of Leeds.
## How to generate comment for corresponding code on T5-small pre-trained model
This is the guide for a interactive demo of generating code comment on T5-small pre-trained model
### Requirements
python 3.6 or above  
torch 1.4 or above  
[transformers](https://github.com/huggingface/transformers)  
  
This demo need to be run on GPU.
### Clone this repository and go to the correspoinding directory
```
git clone https://github.com/Samuel-Fang/AutomaticCodeCommentGeneration
cd AutomaticCodeCommentGeneration/EXPERIMENTS/T5
```
### Run the interactive demo
```
python T5Generate.py
```
## How to test the T5-small pre-trained model on test dataset
### Requirements
python 3.6 or above  
torch 1.4 or above  
[transformers](https://github.com/huggingface/transformers)  
ntlk  
rouge  
  
The test need to be run on GPU.
### Clone this repository and go to the correspoinding directory
```
git clone https://github.com/Samuel-Fang/AutomaticCodeCommentGeneration
cd AutomaticCodeCommentGeneration/EXPERIMENTS/T5
```
### Run the test
```
./test.sh 0,1 CSNpython T5-small CSNpyEx2
```

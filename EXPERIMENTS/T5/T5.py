from transformers import *
import pandas as pd
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import tqdm
from nltk.translate.bleu_score import corpus_bleu
from rouge import FilesRouge
import logging
import sys
import os
from argparse import ArgumentParser

class CodeCommentData(Dataset):
    def __init__(self, df):
        self.df = df
        self.tokenizer = tokenizer
        
    def __getitem__(self, index):
        code_subtokens_ids = self.df['code_subtokens_ids'][index]
        code_subtokens_mask = self.df['code_subtokens_mask'][index]
        #comment = {'input_ids': self.df['comment_ids'][index], 'attention_mask': self.df['comment_mask'][index]}
        comment_ids = self.df['comment_ids'][index]
        comment_mask = self.df['comment_mask'][index]

        return {
            'input_ids': code_subtokens_ids,
            'attention_mask': code_subtokens_mask,
            'labels': comment_ids,
            'decoder_attention_mask': comment_mask
        }

    def __len__(self):
        return len(self.df)

def setDataset(tokenizer):
    subtokens = [None, None, None]
    comments = [None, None, None]

    for index, datatype in enumerate(['train', 'valid', 'test']):
        logger.info('processing %s data...'%datatype)

        subtokenfile = './data/{}/{}/code.original_subtoken'.format(args.dataset, datatype)
        javadocfile = './data/{}/{}/javadoc.original'.format(args.dataset, datatype)

        sf = open(subtokenfile, 'r')
        jf = open(javadocfile, 'r')

        subtokens[index] = []
        comments[index] = []

        i = 0
        if datatype=='train':
            if args.only_test:
                volume = 10
            else:
                volume =64000
        if datatype=='valid':
            if args.only_test:
                volume = 10
            else:
                volume = 800
        if datatype=='test': volume = 1000

        for sline, cline in zip(sf, jf):
            #print(len(tokenizer(sline.strip())['input_ids']))
            if not len(tokenizer(sline.strip())['input_ids'])>512:
                subtokens[index].append(sline.strip())
                comments[index].append(cline.strip())
                i+=1
            if not i<volume: break

        logger.info('tokenizing...')
        subtokens[index] = tokenizer(subtokens[index], padding=True)
        comments[index] = tokenizer(comments[index], padding=True)

    train = {'code_subtokens_ids': subtokens[0]['input_ids'], 'code_subtokens_mask': subtokens[0]['attention_mask'], 'comment_ids': comments[0]['input_ids'], 'comment_mask': comments[0]['attention_mask']}
    valid = {'code_subtokens_ids': subtokens[1]['input_ids'], 'code_subtokens_mask': subtokens[1]['attention_mask'], 'comment_ids': comments[1]['input_ids'], 'comment_mask': comments[1]['attention_mask']}
    test = {'code_subtokens_ids': subtokens[2]['input_ids'], 'code_subtokens_mask': subtokens[2]['attention_mask'], 'comment_ids': comments[2]['input_ids'], 'comment_mask': comments[2]['attention_mask']}

    train_df = pd.DataFrame(train, columns=['code_subtokens_ids', 'code_subtokens_mask', 'comment_ids', 'comment_mask'])
    valid_df = pd.DataFrame(valid, columns=['code_subtokens_ids', 'code_subtokens_mask', 'comment_ids', 'comment_mask'])
    test_df = pd.DataFrame(test, columns=['code_subtokens_ids', 'code_subtokens_mask', 'comment_ids', 'comment_mask'])

    train_dataset = CodeCommentData(train_df)
    valid_dataset = CodeCommentData(valid_df)
    test_dataset = CodeCommentData(test_df)

    del train, valid, test, train_df, valid_df, test_df
    return train_dataset, valid_dataset, test_dataset

def new_report(test_report):
    lists = os.listdir(test_report)
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))
    file_new = os.path.join(test_report, lists[-1])
    print(file_new)
    return file_new


if __name__ == "__main__":
    # set args
    parser = ArgumentParser()
    parser.add_argument('-m', '--model', dest='model',
                        help='The pretrained model name')
    parser.add_argument('-e', '--experiment', dest='experiment',
                        help='The experiment name')
    parser.add_argument('-d', '--data', dest='dataset',
                        help='The dataset of the experiment')
    parser.add_argument('-t', '--test', dest='only_test', default=False,
                        help='only test or not')
    args = parser.parse_args()


    # set logger
    logger = logging.getLogger()
    log_file = 'results/%s/log.txt'%args.experiment

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s: [ %(message)s ]',
                            '%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    logfile = logging.FileHandler(log_file, 'a')
    logfile.setFormatter(fmt)
    logger.addHandler(logfile)

    logger.info('COMMAND: %s' % ' '.join(sys.argv))


    tokenizer = T5Tokenizer.from_pretrained(args.model)
    #tokenizer.pad_token = tokenizer.eos_token
    train_dataset, valid_dataset, test_dataset= setDataset(tokenizer)
    logger.info('dataset is ready')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info('The training is running on %s'%device)

    model = T5ForConditionalGeneration.from_pretrained(args.model)
    model = model.to(device)


    def compute_metrics(pred):
        labels = output_dir+'/labels.txt'
        preds = output_dir+'/preds.txt'
        lf = open(labels, 'w')
        pf = open(preds, 'w')
        labels_list = []
        preds_list = []

        for label, pred in zip(pred.label_ids, pred.predictions):
            de_label = tokenizer.decode(label)
            de_pred = tokenizer.decode(pred.argmax(-1))
            lf.write(de_label+'\n')
            pf.write(de_pred+'\n')
            labels_list.append([de_label])
            preds_list.append(de_pred)

        lf.close()
        pf.close()

        bleu_score = corpus_bleu(labels_list, preds_list)
        files_rouge = FilesRouge()
        rouge_score = files_rouge.get_scores(preds, labels, avg=True)


        return {
            'bleu score: ': bleu_score*100,
            'rouge-l: ': rouge_score['rouge-l']['f']*100
        }

    output_dir = './results/%s'%args.experiment

    if not args.only_test:

        logger.info('start trianing...')
        if not os.path.exists(output_dir+'/model'):
            training_args = TrainingArguments(
                output_dir=output_dir+'/model',
                per_device_train_batch_size=16,
                per_device_eval_batch_size=2,
                num_train_epochs=100,
                logging_dir=output_dir+'/logs',
                evaluate_during_training=True,
                logging_steps=2000,
                save_total_limit=20,
                save_steps=2000,
                eval_steps=2000
            )
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=valid_dataset,
                compute_metrics=compute_metrics
            )

            logger.info('training from scratch...')
            trainer.train()
        else:
            training_args = TrainingArguments(
                output_dir=output_dir+'/model',
                per_device_train_batch_size=16,
                per_device_eval_batch_size=1,
                num_train_epochs=100,
                logging_dir=output_dir+'/logs',
                evaluate_during_training=True,
                logging_steps=2000,
                save_total_limit=20,
                save_steps=2000,
                eval_steps=2000,
                overwrite_output_dir=True
            )
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=valid_dataset,
                compute_metrics=compute_metrics
            )

            checkpoint_dir = new_report(output_dir+'/model')
            logger.info('training from checkpoint...')
            trainer.train(checkpoint_dir)

        trainer.save_model(output_dir+'/model')

    else:
        training_args = TrainingArguments(
            output_dir=output_dir+'/model',
            per_device_train_batch_size=16,
            per_device_eval_batch_size=1,
            num_train_epochs=100,
            logging_dir=output_dir+'/logs',
            evaluate_during_training=True,
            logging_steps=2000,
            save_total_limit=20,
            save_steps=2000,
            eval_steps=2000
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=valid_dataset,
            compute_metrics=compute_metrics
        )

        checkpoint_path = output_dir+'/model/checkpoint-34000/pytorch_model.bin'
        model.load_state_dict(torch.load(checkpoint_path))

        #predictions, label_ids, metrics = trainer.predict(test_dataset)
        #logger.info('Test results: ', metrics)

        predictResult = trainer.predict(test_dataset)
        logger.info(predictResult)
import ast
import json
from argparse import ArgumentParser

#filename = 'CSNparse.py'
#jsonfile = './test/python_test_0.jsonl'

def read_file_to_string(filename):
    f = open(filename, 'rt')
    s = f.read()
    f.close()
    return s

def jsonToPy(jsonfile, save):
    with open(jsonfile, 'r', encoding='utf-8') as f:
        i = 0
        for line in f:
            fuc = json.loads(line.strip())
            '''savefile = './{}PyFile/sourceCode{}.py'.format(save, i)
            sf = open(savefile, 'w')
            sf.write(fuc['code'])'''

            targetfile = '{}_target_raw.txt'.format(save)
            tarf = open(targetfile, 'a')
            tar = fuc['docstring']
            tarT = fuc['docstring_tokens']
            if not (('\n' in tar) or ('http' in tar) or ('(' in tar) or (')' in tar) or ('[' in tar) or (']' in tar) or (':' in tar) or (len(tarT)<4)):
                if i==0:
                    tarf.write(tar)
                else:
                    tarf.write('\n'+'\n'+tar)
                i+=1

parser = ArgumentParser()
parser.add_argument('-d', '--data', dest='data',
                    help='json to python files for which dataset')
args = parser.parse_args()

if args.data=='train':
    for i in range(14):
        jsonfile = './{}/python_{}_{}.jsonl'.format(args.data, args.data, str(i))
        jsonToPy(jsonfile, args.data+str(i))
else:
    jsonfile = './{}/python_{}_0.jsonl'.format(args.data, args.data)
    jsonToPy(jsonfile, args.data)



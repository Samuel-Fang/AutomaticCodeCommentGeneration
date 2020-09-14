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

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def clean(strSeq):
    dirt = ['\n', 'http', '(', ')', '[', ']', '/', '\\', ':', '<', '>']
    keep = True
    if not isEnglish(strSeq): keep = False
    for d in dirt:
        if d in strSeq: keep = False
    return keep

def jsonToPy(jsonfile, save):
    with open(jsonfile, 'r', encoding='utf-8') as f:
        i = 0
        for line in f:
            fuc = json.loads(line.strip())
            if clean(fuc['docstring']) and not len(fuc['docstring_tokens'])<4:
                savefile = './{}PyFile/sourceCode{}.py'.format(save, i)
                sf = open(savefile, 'w')
                sf.write(fuc['code'])

                targetfile = '{}_target_raw.json'.format(save)
                tarf = open(targetfile, 'a')
                tar = {}
                tar['docstring'] = fuc['docstring_tokens']
                jsonwrite = json.dumps(tar, separators=(',', ':'), ensure_ascii=False)
                if i==0:
                    tarf.write(jsonwrite)
                else:
                    tarf.write('\n'+jsonwrite)
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



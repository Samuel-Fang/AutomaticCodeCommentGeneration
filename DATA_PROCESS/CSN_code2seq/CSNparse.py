from argparse import ArgumentParser
import json
import parse_python as par

def ast_python(jsonfile, savefile):
    with open(jsonfile, 'r', encoding='utf-8') as f:
            for line in f:
                fuc = json.loads(line.strip())
                tree = par.parse_file(jsonfile, fuc['code'])

                with open(savefile, 'a') as sf:
                    sf.write(tree)
                    sf.close()
            f.close()

def clearJson(savefile):
    with open(savefile, 'r+') as f:
        f.seek(0)
        f.truncate()
        f.close()

def main():
    parser = ArgumentParser()
    '''parser.add_argument('--train', dest='train', 
                        help='create ast for train data')
    parser.add_argument('--valid', dest='valid', 
                        help='create ast for valid data')
    parser.add_argument('--test', dest='test', 
                        help='create ast for test data')'''
    parser.add_argument('-d', '--data', dest='data',
                        help='create ast for which dataset')
    args = parser.parse_args()
    
    if args.data=='train':
        savefile = 'test_ast.json'
        clearJson(savefile)
        for i in range(14):
            jsonfile = './train/python_valid_{}.jsonl'.format(i)
            ast_python(jsonfile, savefile)
    else:
        if args.data=='test':
            jsonfile = './test/python_test_0.jsonl'
            savefile = 'test_ast.json'
        if args.data=='valid':
            jsonfile = './valid/python_valid_0.jsonl'
            savefile = 'valid_ast.json'

        #clearJson(savefile)
        ast_python(jsonfile, savefile)

        '''CSN = []
        with open(jsonfile, 'r', encoding='utf-8') as f:
            for line in f:
                fuc = json.loads(line.strip())
                CSN.append(fuc)

                tree = par.parse_file()

        print(CSN[0])
        print(CSN[0]['code'])'''

if __name__ == "__main__":
    main()
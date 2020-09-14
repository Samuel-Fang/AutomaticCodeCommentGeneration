from argparse import ArgumentParser
import json
import parse_python as par
import os

def ast_python(codedir, savefile, datatype):
    dirs = os.listdir(codedir)
    for i in dirs:
         if os.path.splitext(i)[1] == ".py":
            try:
                tree = par.parse_file(codedir+'/'+i)
                with open(savefile, 'a') as sf:
                        sf.write(tree+'\n')
                        sf.close()
                target_process(int(i[10:-3]), datatype)
            except SyntaxError as err:
                print(err)

def target_process(index, datatype):    
    tarFile = '{}_target_raw.json'.format(datatype)
    if len(datatype)>5: datatype = datatype[:5]
    tarSaveFile = '{}_target_finish.json'.format(datatype)

    tarf = open(tarFile, 'r')
    lines = tarf.readlines()
    tarsf = open(tarSaveFile, 'a')

    jsonline = json.loads(lines[index].strip())['docstring']
    target = jsonline[0]
    for s in jsonline[1:]:
        target = target+'|'+s
    jsontar = {}
    jsontar['docstring'] = target
    jsonwrite = json.dumps(jsontar, separators=(',', ':'), ensure_ascii=False)
    tarsf.write(jsonwrite+'\n')
            


def clearJson(savefile):
    if os.path.exists(savefile):
        with open(savefile, 'r+') as f:
            f.seek(0)
            f.truncate()
            f.close()

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--data', dest='data',
                        help='create ast for which dataset')
    args = parser.parse_args()
    


    dt = args.data
    if len(dt)>5: dt = dt[:5]
    codedir = './{}PyFile'.format(args.data)
    savefile = '{}_ast.json'.format(dt)

    #clearJson(savefile)
    ast_python(codedir, savefile, args.data)


if __name__ == "__main__":
    main()
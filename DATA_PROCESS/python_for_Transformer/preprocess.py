import json
import re
from tqdm import tqdm

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

def cleanCode(code):
    cleanedCode = []
    for token in code:
        if not (('\n' in token) or ('https://github' in token) or ('\r' in token) or ('# ' in token)):
            cleanedCode.append(token)
    return cleanedCode

def tokenize_with_camel_case(token):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', token)
    return [m.group(0) for m in matches]

def tokenize_with_snake_case(token):
    return token.split('_')

def subtoken_spliter(tokens):
    snakeSubtokens = []
    for token in tokens:
        snakeSubtokens.extend(tokenize_with_snake_case(token))
    camelSubtokens = []
    for token in snakeSubtokens:
        camelSubtokens.extend(tokenize_with_camel_case(token))
    subtokens = camelSubtokens
    return subtokens

def writeTokens(tokens, f):
    i = 0
    for token in tokens:
        if i==0: f.write(token)
        else: f.write(' '+token)
        i+=1
    f.write('\n')


def preprocess(input, output):
    inputfile = output+'/python_'+input+'.jsonl'
    codefile = 'python/'+output+'/code.original'
    subtokenfile = 'python/'+output+'/code.original_subtoken'
    javadocfile = 'python/'+output+'/javadoc.original'

    fc = open(codefile, 'a')
    fs = open(subtokenfile, 'a')
    fj = open(javadocfile, 'a')

    with open(inputfile, 'r', encoding='utf-8') as f:
        pbar = tqdm(f.readlines())
        pbar.set_description('preprocessing %s'%input)
        for line in pbar:
            fuc = json.loads(line.strip())
            if clean(fuc['docstring']) and not len(fuc['docstring_tokens'])<4 and not len(fuc['docstring_tokens'])>30 and not len(fuc['code_tokens'])>450:
                codetokens = cleanCode(fuc['code_tokens'])
                writeTokens(codetokens, fc)

                subtokens = subtoken_spliter(codetokens)
                writeTokens(subtokens, fs)

                writeTokens(fuc['docstring_tokens'], fj)

    fc.close()
    fs.close()
    fj.close()

if __name__ == "__main__":
    preprocess('test_0', 'test')
    preprocess('valid_0', 'valid')
    for i in range(14):
        input = 'train_'+str(i)
        preprocess(input, 'train')


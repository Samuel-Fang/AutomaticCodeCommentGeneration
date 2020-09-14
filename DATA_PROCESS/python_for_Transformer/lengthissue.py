import json

datafile = 'test/python_test_0.jsonl'

count = 0
with open(datafile, 'r', encoding='utf-8') as f:
    for line in f:
        fuc = json.loads(line.strip())
        for token in fuc['code_tokens']:
            if ' ' in token:
                if not '\n' in token and not '\r' in token:
                    if not '# ' in token:
                        print(token)
                        count+=1


print(count)
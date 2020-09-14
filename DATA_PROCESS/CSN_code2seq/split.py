input = 'I love UUU \'and\' it-is a great_thing do `you` know it.'

'''splits = input.split()
if splits[-1][-1]=='.':
    splits[-1] = splits[-1][:-1]
    splits.append('.')
print('|'.join(split.lower() for split in splits))'''

input = input.replace('-', ' ')
input = input.replace('_', ' ')
input = input.replace('.', '')
input = input.replace('`', '')
input = input.replace('\'', '')

print(input)

splits = input.split()

print('|'.join(split.lower() for split in splits))
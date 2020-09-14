random_numbers = [3710, 4240, 6074, 4308, 5758, 5500, 2927, 1689, 3249, 903]

code_file = './CSNpython/test/code.original'
sub_file = './CSNpython/test/code.original_subtoken'
doc_file = './CSNpython/test/javadoc.original'

cf = open(code_file, 'r')
sf = open(sub_file, 'r')
df = open(doc_file, 'r')

codes = []
subs = []
docs = []

for lineC, lineS, lineD in zip(cf.readlines(), sf.readlines(), df.readlines()):
    codes.append(lineC.strip())
    subs.append(lineS.strip())
    docs.append(lineD.strip())

output_code = 'qualititative_code.txt'
output_sub = 'qulititative_subtoken.txt'
output_doc = 'qualititative_doc.txt'

ocf = open(output_code, 'a')
osf = open(output_sub, 'a')
odf = open(output_doc, 'a')

for number in random_numbers:
    ocf.write(codes[number-1]+'\n')
    osf.write(subs[number-1]+'\n')
    odf.write(docs[number-1]+'\n')
    print(len(subs[number-1].split()))
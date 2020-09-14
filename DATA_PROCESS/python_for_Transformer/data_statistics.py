import matplotlib.pyplot as plt

def statistics(trainfile, testfile, devfile):
    lens = []
    maxlen = 0
    sumlen = 0
    i = 0
    for datafile in (trainfile, testfile, devfile):
        with open(datafile, 'r') as f:
            for line in f:
                splits = line.strip().split()
                leng = len(splits)
                lens.append(leng)
                if leng>maxlen: maxlen = leng
                if leng>600:
                    print(splits)
                    print('\n')
                sumlen = sumlen + leng
                i+=1
    avglen = sumlen/i
    plt.hist(lens, bins=20)
    print('\n')

    return maxlen, avglen

if __name__ == "__main__":
    outputfile = 'data_statistics.txt'
    wf = open(outputfile, 'a')

    plt.clf()
    codemax, codeavg = statistics('CSNpython/train/code.original', 'CSNpython/test/code.original', 'CSNpython/dev/code.original')
    wf.write('code tokens statics: max length: '+str(codemax)+' average length: '+str(codeavg)+'\n')
    plt.savefig('pic/code_tokens_statistics.png')

    plt.clf()
    subtokenmax, subtokenavg = statistics('CSNpython/train/code.original_subtoken', 'CSNpython/test/code.original_subtoken', 'CSNpython/dev/code.original_subtoken')
    wf.write('code subtokens statics: max length: '+str(subtokenmax)+' average length: '+str(subtokenavg)+'\n')
    plt.savefig('pic/code_subtokens_statistics.png')

    plt.clf()
    docmax, docavg = statistics('CSNpython/train/javadoc.original', 'CSNpython/test/javadoc.original', 'CSNpython/dev/javadoc.original')
    wf.write('javadoc statics: max length: '+str(docmax)+' average length: '+str(docavg)+'\n')
    plt.savefig('pic/javadoc_statistics.png')

    wf.close()

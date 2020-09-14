files = ['train_output_file.txt', 'valid_output_file.txt', 'test_output_file.txt']

count = 0
pathcount = 0
pathsum = 0
pathlensum = 0
targetlensum = 0

for filename in files:
    f = open(filename, 'r')
    for line in f:
        paths = line.strip().split()
        target = paths[0]

        pathnum = len(paths)-1
        pathsum = pathsum + pathnum
        targetlen = len(target.split('|'))
        targetlensum = targetlen + targetlensum
        for path in paths[1:]:
            pathcount+=1
            pathlen = len(path)
            pathlensum = pathlen + pathlensum
        count+=1

print('Average path amount is: ', pathsum/count)
print('Average path length is: ', pathlensum/pathcount)
print('Average target lenghth is: ', targetlensum/count)

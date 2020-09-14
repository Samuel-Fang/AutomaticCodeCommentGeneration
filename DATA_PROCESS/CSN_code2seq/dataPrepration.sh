mkdir testPyFile
mkdir validPyFile

mkdir train0PyFile
mkdir train1PyFile
mkdir train2PyFile
mkdir train3PyFile
mkdir train4PyFile
mkdir train5PyFile
mkdir train6PyFile
mkdir train7PyFile
mkdir train8PyFile
mkdir train9PyFile
mkdir train10PyFile
mkdir train11PyFile
mkdir train12PyFile
mkdir train13PyFile

python jsonToPy.py -d test
2to3 testPyFile/
python CSNparser.py -d test

python jsonToPy.py -d valid
2to3 validPyFile/
python CSNparser.py -d valid

python jsonToPy.py -d train

2to3 train0PyFile/
python CSNparser.py -d train0
2to3 train1PyFile/
python CSNparser.py -d train1
2to3 train2PyFile/
python CSNparser.py -d train2
2to3 train3PyFile/
python CSNparser.py -d train3
2to3 train4PyFile/
python CSNparser.py -d train4
2to3 train5PyFile/
python CSNparser.py -d train5
2to3 train6PyFile/
python CSNparser.py -d train6
2to3 train7PyFile/
python CSNparser.py -d train7
2to3 train8PyFile/
python CSNparser.py -d train8
2to3 train9PyFile/
python CSNparser.py -d train9
2to3 train10PyFile/
python CSNparser.py -d train10
2to3 train11PyFile/
python CSNparser.py -d train11
2to3 train12PyFile/
python CSNparser.py -d train12
2to3 train13PyFile/
python CSNparser.py -d train13
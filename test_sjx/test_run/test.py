import csv
import json
import os

# path = os.getcwd()
# p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
# configfilepath = p + "\\test_config\\userconfig1.csv"
# configfile = open(configfilepath, 'r')
# table = csv.reader(configfile)
# num=0
# lis=[]
# for i in table:
#     if num==0:
#         casenum = i[0]
#         casename = i[1]
#         apiname=i[3]
#         apipath=i[4]
#         expect=i[13]
#         #print(casenum, casename,apiname,apipath)
#         lis.append(casenum)
#         lis.append(casename)
#         lis.append(apiname)
#         lis.append(apipath)
#         lis.append('请求参数')
#         lis.append('请求耗时')
#         lis.append(expect)
#         lis.append('实际返回结果')
#         print(lis)
#     num=num+1

# title = list(table)[0]
# print(title)
path = os.getcwd()
p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
txtfilepath = p + "\\test_temporary\\tmp.txt"
tmpfile = open(txtfilepath, 'r')
result = eval(tmpfile.read())
for i in result.keys():
    print(i)
for a in result.values():
    print(a)

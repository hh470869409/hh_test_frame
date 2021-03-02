import csv
import datetime
import hashlib
import json
import requests
from test_run.test_frame import report, filepath


class testquery():
    def test_userinfo(self):
        filepathobj=filepath()
        filepathobj.read_filepath()
        file=open(filepathobj.filepath,'r')
        table=csv.reader(file)
        header=next(table)
        repobj = report()
        for row in table:
            statrtime = datetime.datetime.now()
            self.url=row[5]
            # 待加密信息
            config = {"serialnumber":row[7],"appcode":row[8],"body":{"identity":row[10],"name":row[9],"mobile":row[11]}}
            strconfig=(json.dumps(config,ensure_ascii=False)+str(row[12])).replace(" ","")
            hl = hashlib.md5()
            hl.update(strconfig.encode(encoding='utf-8'))
            MD5=hl.hexdigest()
            #print('MD5加密前为 ：' + strconfig)
            #print('MD5加密后为 ：' + MD5)
            request={"serialnumber":row[7],"appcode":row[8],"body":{"identity":row[10],"name":row[9],"mobile":row[11]},"sign":MD5}
            self.userinfo=json.dumps(request,ensure_ascii=False).replace(" ","")

            hader={
                "Content-Type":"application/json"
            }
            self.response=requests.post(self.url,data=self.userinfo.encode('utf-8'),headers=hader).text
            endtime = datetime.datetime.now()
            difftime = (endtime - statrtime).microseconds*0.000001
            repobj.addresult(str(self.userinfo),str(self.response))
            repobj.readresult()
            repobj.writeresult(row[0], row[1], row[3], row[4], str(self.userinfo), difftime, row[13], str(self.response))
            print(self.userinfo,self.response)


if __name__=='__main__':
    obj=testquery()
    obj.test_userinfo()






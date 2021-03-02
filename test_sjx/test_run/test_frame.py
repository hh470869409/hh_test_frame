import csv
import datetime
import os
import wx

class UI_frame():
    def __init__(self):
        # 定义窗体及容器
        self.app=wx.App()
        self.window=wx.Frame(None,title='自动化测试框架',size=(650,300))
        self.panel=wx.Panel(self.window)

        #定义窗体控件
        #标签文字
        self.label_file=wx.StaticText(self.panel,label='测试用例执行文件')
        #文件显示文本框
        self.csv_file=wx.TextCtrl(self.panel,style=wx.TE_READONLY)
        #打开按钮
        self.button_open=wx.Button(self.panel,label='打开文件')
        #执行按钮
        self.button_run = wx.Button(self.panel, label='执行')
        #重置按钮
        self.button_reset = wx.Button(self.panel, label='重置')
        #退出按钮
        self.button_exit = wx.Button(self.panel, label='退出')

    #控件布局
    def UI_layout(self):
        #水平布置第一行
        boxsizer1=wx.BoxSizer()
        boxsizer1.Add(self.label_file,flag=wx.ALL,border=13)
        boxsizer1.Add(self.csv_file,flag=wx.ALL|wx.EXPAND,proportion=1,border=10)
        boxsizer1.Add(self.button_open, flag=wx.ALL, border=10)

        #水平布置第二行
        boxsizer2=wx.BoxSizer()
        boxsizer2.Add(self.button_run,flag=wx.LEFT,border=80)
        boxsizer2.Add(self.button_reset,flag=wx.LEFT,border=100)
        boxsizer2.Add(self.button_exit,flag=wx.LEFT,border=100)

        #把前两行放到垂直布局里面
        boxsizer3=wx.BoxSizer(wx.VERTICAL)
        boxsizer3.Add(boxsizer1,flag=wx.ALL|wx.EXPAND,border=10)
        boxsizer3.Add(boxsizer2,flag=wx.ALL,border=40)

        #生效
        self.panel.SetSizer(boxsizer3)

    #显示窗体
    def UI_show(self):
        self.window.Show(True)
        self.app.MainLoop()

    #按钮出发绑定事件
    def UI_event(self):
        #打开按钮
        self.button_open.Bind(wx.EVT_BUTTON,self.openfile)
        #执行按钮
        self.button_run.Bind(wx.EVT_BUTTON,self.rundriver)
        #重置按钮
        self.button_reset.Bind(wx.EVT_BUTTON,self.reset)
        #退出按钮
        self.button_exit.Bind(wx.EVT_BUTTON,self.exit)

    #打开文件按钮事件
    def openfile(self,event):
        pathobj=filepath()
        #设置打开文件对话框
        self.csvopen=wx.FileDialog(self.panel,message="打开文件",wildcard="*csv",style=wx.FD_OPEN)
        #如果点击确定，把文件路径放入对话框中
        if self.csvopen.ShowModal()==wx.ID_OK:
            self.csv_file.AppendText(self.csvopen.GetPath())
            #获取执行文件的路径
            self.configpath=self.csvopen.GetPath()
            pathobj.add_filepath(self.configpath)

    #执行按钮事件
    def rundriver(self,event):
        csv=self.csv_file.GetValue()
        if csv=='':
            ermessages=wx.GenericMessageDialog(None,"配置文件不能为空","错误提示",wx.YES_DEFAULT|wx.ICON_QUESTION)
            if ermessages.ShowModal()==wx.ID_YES:
                ermessages.Destroy()
            return 0
        else:
            #执行驱动程序
            runfileobj=driver_frame()
            runfileobj.runfile(self.configpath)

    #重置按钮事件
    def reset(self,event):
        self.csv_file.SetValue('')

    #退出按钮事件
    def exit(self,event):
        self.window.Close()

#驱动类
class driver_frame():
    #执行方法
    def runfile(self,config):
        reportobj = report()
        reportobj.createreport()
        reportobj.writetitle()
        file = open(config, 'r')
        table = csv.reader(file)
        header = next(table)
        for row in table:
            # statrtime = datetime.datetime.now()
            # 执行脚本
            if row[2]!="":
                runOS = 'python ' + row[2]
                os.system(runOS)

class report():
    def createreport(self):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        filepath = p + "\\test_report\\report.csv"
        if os.path.exists(filepath):
            os.remove(filepath)
        self.reportfile = open(filepath, 'a', newline='')
        self.write = csv.writer(self.reportfile)

    def writetitle(self):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        configfilepath = p + "\\test_config\\userconfig1.csv"
        configfile = open(configfilepath, 'r')
        table = csv.reader(configfile)
        num = 0
        lis = []
        for i in table:
            if num == 0:
                casenum = i[0]
                casename = i[1]
                apiname = i[3]
                apipath = i[4]
                expect = i[13]
                # print(casenum, casename,apiname,apipath)
                lis.append(casenum)
                lis.append(casename)
                lis.append(apiname)
                lis.append(apipath)
                lis.append('请求参数')
                lis.append('请求耗时(秒)')
                lis.append(expect)
                lis.append('实际返回结果')
            num = num + 1
        self.write.writerow(lis)
        self.reportfile.close()

    def addresult(self,request,response):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        txtfilepath = p + "\\test_temporary\\tmp.txt"
        tmpfile=open(txtfilepath,'w')
        tmpfile.write(request+'\n')
        tmpfile.write(response+ '\n')
        tmpfile.close()

    def readresult(self):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        txtfilepath = p + "\\test_temporary\\tmp.txt"
        tmpfile = open(txtfilepath, 'r')
        result = tmpfile.read().split("\n")
        self.request = result[0]
        self.response = result[1]


    def writeresult(self,casenum,casename,apiname,apipath,request,difftime,expect,response):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        filepath = p + "\\test_report\\report.csv"
        self.reportfile=open(filepath,'a',newline='')
        self.write=csv.writer(self.reportfile)
        self.write.writerow([casenum,casename,apiname,apipath,request,difftime,expect,response])
        self.reportfile.close()



class filepath():
    def add_filepath(self,filepath):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        txtfilepath = p + "\\test_temporary\\filepath.txt"
        tmpfile = open(txtfilepath, 'w')
        tmpfile.write(filepath)
        tmpfile.close()

    def read_filepath(self):
        path = os.getcwd()
        p = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        txtfilepath = p + "\\test_temporary\\filepath.txt"
        tmpfile = open(txtfilepath, 'r')
        result = tmpfile.read().split("\n")
        self.filepath=result[0]





if __name__=='__main__':
    UIobj = UI_frame()
    UIobj.UI_layout()
    UIobj.UI_event()
    UIobj.UI_show()

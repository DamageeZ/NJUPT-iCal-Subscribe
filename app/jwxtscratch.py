import requests
import re
import ddddocr
from lxml import etree
import configparser
import sys, os, getopt
from iGenerator import IcsGenerator

sStartTime = (2023, 2, 13) # 必须是周一
classSTime = [(8, 0), (8, 50), (9, 50), (10, 40), (11, 30),
            (13, 45), (14, 35), (15, 35), (16, 25), 
            (18, 30), (19, 25), (20, 20)]
classDuration = 45

class Scratcher():
    def __init__(self, xh, pswd, baseUrl="http://jwxt.njupt.edu.cn/", loginSubUrl="default2.aspx"):
        print("爬取启动")
        self.ocr = ddddocr.DdddOcr(show_ad=False)
        self.baseUrl = baseUrl
        self.xh = xh
        self.session = requests.session()
        self.headers = {
            "Referer":"http://jwxt.njupt.edu.cn/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0"
        }
        self.get_VIEWSTATE(self.session.get(url=self.baseUrl, headers=self.headers))
        data={
            '__VIEWSTATE': self.VIEWSTATE,
            'txtUserName': xh,
            'TextBox2': pswd ,
            'txtSecretCode': self.ocr.classification(self.get_checkCode()),
            'RadioButtonList1': u"学生".encode("gb2312", 'replace'),
            'Button1':'',
            'lbLanguage':'',
            'hidPdrs':'',
            'hidsc':''
        }
        loginResp = self.session.post(url=self.baseUrl+loginSubUrl, data=data, headers=self.headers)
        if loginResp.url.find(loginSubUrl) != -1:
            raise Exception("LoginFailed")
        Parser = etree.HTML(loginResp.text)
        self.name = Parser.xpath("//*[@id='xhxm']/text()")[0][:-2]
        self.links = {a.text:self.baseUrl+a.attrib.get('href') for a in Parser.xpath("//li[@class='top']/ul[@class='sub']//a")}
        self.iGenerator = IcsGenerator(sStartTime, self.xh, classSTime, classDuration)

    def get_checkCode(self, suburl="CheckCode.aspx?"):
        return self.session.get(url=self.baseUrl+suburl).content
    
    def get_VIEWSTATE(self, resp):
        self.VIEWSTATE=re.findall('<input type="hidden" name="__VIEWSTATE" value=(.*?) />',resp.text)[0][1:-1]
    
    def get_xkqk(self):
        xkqkUrl = self.links["学生选课情况查询"]
        xkqkResp = self.session.get(url=xkqkUrl, headers=self.headers)
        return xkqkResp.text
    
    def generateICS(self):
        return self.iGenerator.genTable(self.get_xkqk()).genStr().extract()

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    opts, args = getopt.getopt(sys.argv[1:], "t", ["xh=", "pswd="])
    optsdict = {opt[0]:opt[1] for opt in opts}
    if "-t" in optsdict.keys():
        xh = optsdict["--xh"]
        pswd = optsdict["--pswd"]
    else:
        config = configparser.ConfigParser()
        config.read("config.conf")
        xh = config.get('user', 'xh')
        pswd = config.get('user', 'pswd')

    try:
        scratcher = Scratcher(xh, pswd)
    except Exception as err:
        print(str(err)+" 请确认学号和密码，或教务系统能够正常访问")
    else:
        with open("t1.ics", "w", encoding='utf8') as f:
            ics = scratcher.generateICS()
            f.write(ics)


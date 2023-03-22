import requests
import re
import ddddocr
from lxml import etree
from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read("config.conf")
txtUserName = config.get('user', 'xh')
TextBox2 = config.get('user', 'pswd')

ocr = ddddocr.DdddOcr(show_ad=False)
session = requests.session()
headers = {
    "Referer":"http://jwxt.njupt.edu.cn/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0"
}

BaseUrl = "http://jwxt.njupt.edu.cn/"
resp = session.get(url=BaseUrl, headers=headers)
VIEWSTATE=re.findall('<input type="hidden" name="__VIEWSTATE" value=(.*?) />',resp.text)[0][1:-1]
# print(VIEWSTATE)

imgeurl='http://jwxt.njupt.edu.cn/CheckCode.aspx?'
imgeread=session.get(url=imgeurl).content
textword = ocr.classification(imgeread)
# with open("a.jpg", 'wb') as f:
#     f.write(imgeread)

data={
    '__VIEWSTATE': VIEWSTATE,
    'txtUserName': txtUserName,
    'TextBox2': TextBox2 ,
    'txtSecretCode': textword,
    'RadioButtonList1': u"学生".encode("gb2312", 'replace'),
    'Button1':'',
    'lbLanguage':'',
    'hidPdrs':'',
    'hidsc':''
}
# print(data)
# headers['Referer'] = "http://jwxt.njupt.edu.cn/"
# inUrl = "http://jwxt.njupt.edu.cn/xs_main.aspx?xh=B20011024"
loginResp = session.post(BaseUrl+"default2.aspx", data=data)
Parser = etree.HTML(loginResp.text)
print("你好，"+Parser.xpath("//*[@id='xhxm']/text()")[0])
# print(Parser.xpath("//li[@class='top']/ul[@class='sub']//a"))
# for a in Parser.xpath("//li[@class='top']/ul[@class='sub']//a"):
#     print(a.text, a.attrib.get('href'))
    
links = {a.text:BaseUrl+a.attrib.get('href') for a in Parser.xpath("//li[@class='top']/ul[@class='sub']//a")}

VIEWSTATE=re.findall('<input type="hidden" name="__VIEWSTATE" value=(.*?) />',loginResp.text)[0][1:-1]

# scheUrl = "http://jwxt.njupt.edu.cn/xskbcx.aspx?xh=B20011024&xm=%D6%DC%D5%DC%C3%F1&gnmkdm=N121603"
# scheResp = session.get(scheUrl, headers=headers)
# with open('schePage.html', 'w') as f:
#     f.write(scheResp.text)
# print(VIEWSTATE)
# print(shResp.text)

classUrl = links["学生选课情况查询"]
classResp = session.get(classUrl, headers=headers)

bs = BeautifulSoup(classResp.text, "lxml")
table = bs.find(id='DBGrid')
tb = []
for idx, tr in enumerate(table.find_all('tr')):
    tb.append([td.text for td in tr.find_all('td')])

# print(tb)
newtb = []
for i in range(len(tb)):
    if i == 0: continue
    time = tb[i][8].replace("\n", "").split(";")
    newtb.append({"ClassID": tb[i][1], 
                  "TeacherName": tb[i][5], 
                  "Time": tb[i][8], 
                  "Classroom": tb[i][9],
                  "NoArg": True if tb[i][16]=="不排课" else False })
for line in newtb:
    if line["NoArg"] == True: 
        continue
    # print(line)
    t = line["Time"].replace("\n", "").split(";")
    pattern = r"周([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u65e5]){1}第(\d{1,2})(,\d{1,2})?(,\d{1,2})?(,\d{1,2})?节"
    print(t)
    p1 = re.compile(pattern=pattern, flags=re.S)
    print([re.match(p1, arg).groups() for arg in t])
# print(classResp.text)
# with open('detailPage.html', 'w') as f:
#     f.write(classResp.text)
# print(loginResp.content.decode('gb2312'))

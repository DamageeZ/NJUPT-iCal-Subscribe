from lxml import etree
from bs4 import BeautifulSoup
import re

# with open('mainPage.html', 'r') as f:
#     pageHtml = f.read()

liWeek = lambda start, end: [i for i in range(int(start), int(end) + 1)]
juWeek = lambda start, end, op: [i for i in range(int(start), int(end) + 1) if (i + op) % 2 == 0] # 1 is odd, 0 is Even
# print(juWeek(2,10,0))

with open('detailPage2.html', 'r', encoding="utf8") as f:
    pageHtml = f.read()

bs = BeautifulSoup(pageHtml, "lxml")
table = bs.find(id='DBGrid')
tb = []
for idx, tr in enumerate(table.find_all('tr')):
    tb.append([td.text for td in tr.find_all('td')])
# print(tb)
# print(tb)
newtb = []
for i in range(len(tb)):
    if i == 0: continue
    if tb[i][16]=="不排课":
        continue
    else:
        newtb.append({"ClassID": tb[i][1], 
                        "ClassName": tb[i][2],
                        "TeacherName": tb[i][5], 
                        "Time": tb[i][8], 
                        "Classroom": tb[i][9]})
# print(newtb)
weekSwitch = {"一":1, "二":2, "三":3, "四":4, "五":5, "六":6, "日":7}
for line in newtb:
    print(line)
    t = line["Time"].strip("\n").split(";")
    pat1 = r"周([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u65e5]){1}第(\d{1,2})(,\d{1,2})?(,\d{1,2})?(,\d{1,2})?节"
    pat2 = r"第(\d{1,2})\-(\d{1,2})周"
    p1 = re.compile(pattern=pat1, flags=re.S)
    p2 = re.compile(pattern=pat2, flags=re.S)
    week = [re.match(p2, arg[arg.find("{") + 1 : arg.find("}")]).groups() for arg in t]
    cArg = [list(re.match(p1, arg).groups()) for arg in t]
    ct = []
    for idx in range(len(t)):
        if t[idx].find("单周") != -1:
            wt = juWeek(*week[idx], 1)
        elif t[idx].find("双周") != -1:
            wt = juWeek(*week[idx], 0)
        else:
            wt = liWeek(*week[idx])
        wd = weekSwitch[cArg[idx].pop(0)]
        cidx = [int(i.replace(',', '')) for i in cArg[idx] if i is not None]
        ct.append([wt, wd, cidx])
    line["Time"] = ct
    line["Classroom"] = line["Classroom"].split(";")
    print(line)
    # print(week)
    # print(cArg)

from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from AppleMapsLoc import AppleLoc

# with open('mainPage.html', 'r') as f:
#     pageHtml = f.read()

liWeek = lambda start, end: [i for i in range(int(start), int(end) + 1)]
juWeek = lambda start, end, op: [i for i in range(int(start), int(end) + 1) if (i + op) % 2 == 0] # 1 is odd, 0 is Even

SStartTime = (2023, 2, 13) # 必须是周一
weekcnt = [SStartTime]
baseline = datetime(*SStartTime)
for i in range(20):
    baseline += timedelta(weeks=1)
    weekcnt.append((baseline.year, baseline.month, baseline.day))
txtUserName = "测试"

classSTime = [(8, 0), (8, 50), (9, 50), (10, 40), (11, 30),
            (13, 45), (14, 35), (15, 35), (16, 25), 
            (18, 30), (19, 25), (20, 20)]
classDuration = 45
# classETime = []
# alloc = datetime(2022,1,1)
# for stime in classSTime:
#     t = alloc + timedelta(hours=stime[0], minutes=stime[1]+classDuration)
#     classETime.append((t.hour, t.minute))

Head = f'''BEGIN:VCALENDAR
METHOD:PUBLISH
CALSCALE:GREGORIAN
PRODID:-//DamageeZ@github.com//NJUPT-iCal-Subscribe//CN
VERSION:2.0
X-APPLE-CALENDAR-COLOR:#0E61B9
X-WR-CALNAME:{txtUserName}的课表
X-WR-TIMEZONE:Asia/Shanghai
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
BEGIN:STANDARD
DTSTART:19890917T020000
RRULE:FREQ=YEARLY;UNTIL=19910914T170000Z;BYMONTH=9;BYDAY=3SU
TZNAME:GMT+8
TZOFFSETFROM:+0900
TZOFFSETTO:+0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19910414T020000
RDATE:19910414T020000
TZNAME:GMT+8
TZOFFSETFROM:+0800
TZOFFSETTO:+0900
END:DAYLIGHT
END:VTIMEZONE
'''
# print(juWeek(2,10,0))

with open('developFolder\detailPage.html', 'r') as f:
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
uidGen = lambda cid, st: cid+"_"+st[:8]+"@DamageeZ.github.com"
runtime = datetime.utcnow().strftime(r"%Y%m%dT%H%M%SZ")

for line in newtb:
    print(line)
    t = line["Time"].strip("\n").split(";")
    pat1 = r"周([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u65e5]){1}第(\d{1,2})(,\d{1,2})?(,\d{1,2})?(,\d{1,2})?节"
    pat2 = r"第(\d{1,2})\-(\d{1,2})周"
    p1 = re.compile(pattern=pat1, flags=re.S)
    p2 = re.compile(pattern=pat2, flags=re.S)
    week = [re.match(p2, arg[arg.find("{") + 1 : arg.find("}")]).groups() for arg in t]
    cArg = [list(re.match(p1, arg).groups()) for arg in t]
    line["Classroom"] = line["Classroom"].replace("－", "-").split(";")
    # ct = []
    for idx in range(len(t)):
        if t[idx].find("单周") != -1:
            wt = juWeek(*week[idx], 1)
        elif t[idx].find("双周") != -1:
            wt = juWeek(*week[idx], 0)
        else:
            wt = liWeek(*week[idx])
        wd = weekSwitch[cArg[idx].pop(0)]
        cidx = [int(i.replace(',', '')) for i in cArg[idx] if i is not None]
        # ct.append([wt, wd, cidx])
        for wk in wt:
            startTime = (datetime(*weekcnt[wk - 1]) + timedelta(days=wd - 1, hours = classSTime[cidx[0] - 1][0], minutes=classSTime[cidx[0] - 1][1])).strftime(r"%Y%m%dT%H%M%S")
            endTime = (datetime(*weekcnt[wk - 1]) + timedelta(days=wd - 1, hours = classSTime[cidx[-1] - 1][0], minutes=classSTime[cidx[-1] - 1][1] + classDuration)).strftime(r"%Y%m%dT%H%M%S")
            Head += f"""BEGIN:VEVENT
CREATED:{runtime}
DESCRIPTION:{"任课老师: " + line["TeacherName"]}
DTEND;TZID=Asia/Shanghai:{endTime}
DTSTAMP:{runtime}
DTSTART;TZID=Asia/Shanghai:{startTime}
LAST-MODIFIED:{runtime}
SEQUENCE:0
SUMMARY:{line["ClassName"] + "@" + line["Classroom"][-3:]}
TRANSP:OPAQUE
UID:{uidGen(line["ClassID"], startTime)}
{AppleLoc(line["Classroom"][idx])}
END:VEVENT
"""

Head += "END:VCALENDAR"

with open("test.ics", 'w', encoding='utf8') as f:
    f.write(Head)
    # print(week)
    # print(cArg)




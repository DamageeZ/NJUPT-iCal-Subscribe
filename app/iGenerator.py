from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from AppleMapsLoc import AppleLoc

liWeek = lambda start, end: [i for i in range(int(start), int(end) + 1)]
juWeek = lambda start, end, op: [i for i in range(int(start), int(end) + 1) if (i + op) % 2 == 0] # 1 is odd, 0 is Even
uidGen = lambda cid, st: cid+"_"+st[:8]+"@DamageeZ.github.com"
weekSwitch = {"一":1, "二":2, "三":3, "四":4, "五":5, "六":6, "日":7}

Head = lambda name : f'''BEGIN:VCALENDAR
METHOD:PUBLISH
CALSCALE:GREGORIAN
PRODID:-//DamageeZ@github.com//NJUPT-iCal-Subscribe//CN
VERSION:2.0
X-APPLE-CALENDAR-COLOR:#0E61B9
X-WR-CALNAME:{name}的课表
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

vevent = lambda rt, tn, et, st, cn, cr, ci: f"""BEGIN:VEVENT
CREATED:{rt}
DESCRIPTION:{"任课老师: " + tn}
DTEND;TZID=Asia/Shanghai:{et}
DTSTAMP:{rt}
DTSTART;TZID=Asia/Shanghai:{st}
LAST-MODIFIED:{rt}
SEQUENCE:0
SUMMARY:{cn + "@" + cr[-3:]}
TRANSP:OPAQUE
UID:{uidGen(ci, st)}
{AppleLoc(cr)}
END:VEVENT
"""

class IcsGenerator():
    def __init__(self, SStartTime:tuple, txtUserName:str, classSTime:list[tuple], classDuration:int):
        self.weekcnt = [SStartTime]
        baseline = datetime(*SStartTime)
        for _ in range(20):
            baseline += timedelta(weeks=1)
            self.weekcnt.append((baseline.year, baseline.month, baseline.day))
        self.classSTime = classSTime
        self.classDuration = classDuration
        self.icsHead = Head(txtUserName)
        self.table = []
        
    def genTable(self, pageHtml):
        bs = BeautifulSoup(pageHtml, "lxml")
        table = bs.find(id='DBGrid')
        tb = []
        for idx, tr in enumerate(table.find_all('tr')):
            tb.append([td.text for td in tr.find_all('td')])
        self.newtb = []
        for i in range(len(tb)):
            if i == 0: continue
            if tb[i][16]=="不排课":
                continue
            else:
                self.newtb.append({"ClassID": tb[i][1], 
                                "ClassName": tb[i][2],
                                "TeacherName": tb[i][5], 
                                "Time": tb[i][8], 
                                "Classroom": tb[i][9]})
        return self
        
    def genStr(self):
        self.icsStr = self.icsHead
        runtime = datetime.utcnow().strftime(r"%Y%m%dT%H%M%SZ")
        for line in self.newtb:
            # print(line)
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
                    startTime = (datetime(*self.weekcnt[wk - 1]) + timedelta(days=wd - 1, hours = self.classSTime[cidx[0] - 1][0], minutes=self.classSTime[cidx[0] - 1][1])).strftime(r"%Y%m%dT%H%M%S")
                    endTime = (datetime(*self.weekcnt[wk - 1]) + timedelta(days=wd - 1, hours = self.classSTime[cidx[-1] - 1][0], minutes=self.classSTime[cidx[-1] - 1][1] + self.classDuration)).strftime(r"%Y%m%dT%H%M%S")
                    self.icsStr += vevent(runtime, line["TeacherName"], endTime, startTime, line["ClassName"], line["Classroom"][idx], line["ClassID"])
        self.icsStr += "END:VCALENDAR"
        return self

    def extract(self):
        return self.icsStr

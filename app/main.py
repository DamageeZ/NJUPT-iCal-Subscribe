from fastapi import FastAPI
from fastapi import Response
from jwxtscratch import Scratcher
import datetime
import os, logging

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch) #将日志输出至屏幕
logger.addHandler(fh) #将日志输出至文件

@app.get("/Njupt-ical.ics")
def icalSubscrib(xh:str, pswd:str, force:bool=False):
    runinfo = ""
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    runtime = datetime.datetime.now()
    runinfo += xh + " "
    if os.access("scratcher.log", os.F_OK) == False:
        f = open("scratcher.log", "w")
        f.close()
    with open("scratcher.log", "r") as f:
        logs = f.readlines()
    found = False
    for idx, log in enumerate(logs):
        log = log.split(";")
        if log[0] == xh:
            lastTime = datetime.datetime(*(int(i) for i in log[1:]))
            found = True
            delta = (runtime-lastTime).seconds
            deltaLimit = 3600
            runinfo += "timeDelta: "+ str(delta) + "/" + str(deltaLimit)
            if force: runinfo += " FORCE"
            if delta >= deltaLimit or force:
                try:
                    scratcher = Scratcher(xh, pswd)
                except Exception as err:
                    errcode = "登录失败 请确认学号和密码，或教务系统能够正常访问"
                    logging.warning(xh+str(err))
                    return Response(content=errcode, media_type="text/plain")
                output = scratcher.generateICS()
                runinfo += " Scraping "
                logs[idx] = ";".join([str(xh), 
                                      str(runtime.year), str(runtime.month), str(runtime.day), 
                                      str(runtime.hour), str(runtime.minute), str(runtime.second)])+"\n"
                break
            else:
                runinfo += " LocalRead "
                f = open(xh+".ics", "r", encoding='utf8')
                output = f.read()
                f.close()
                break
    # logs[logid] = ";".join([str(xh), str(runtime.year), str(runtime.month), str(runtime.day), str(runtime.hour), str(runtime.minute)])+"\n"
    print(found)
    # print(logs)
    if not found:
        logs.append(";".join([str(xh), 
                              str(runtime.year), str(runtime.month), str(runtime.day), 
                              str(runtime.hour), str(runtime.minute), str(runtime.second)])+"\n")
        try:
            scratcher = Scratcher(xh, pswd)
        except Exception as err:
            errcode = "登录失败 请确认学号和密码，或教务系统能够正常访问"
            logging.warning(xh+str(err))
            return Response(content=errcode, media_type="text/plain")
        output = scratcher.generateICS()
    with open("scratcher.log", "w") as f:
        f.writelines(logs)
    with open(xh+".ics", "w", encoding='utf8') as f:
        f.write(output)
    logger.info(runinfo)
    return Response(content=output, media_type="text/plain")

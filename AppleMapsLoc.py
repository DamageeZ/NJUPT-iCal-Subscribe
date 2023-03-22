AppleMaps = lambda loc : [
    {
        "judge": "教1" in loc,
        "raw": r"""LOCATION:南京邮电大学仙林校区教1号楼\n文苑路9号(近南京财经大学仙林校区)
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=52.04841949714999;X-APPLE-REFERENCEFRAME=2;X-TITLE=南京邮电大学仙林校区教1号楼\\n文苑路9号(近南京财经大学仙林校区):geo:32.107141,118.930790"""
    },
    {
        "judge": "教2" in loc,
        "raw": r"""
"""
    },
    {
        "judge": "教3" in loc,
        "raw": r"""LOCATION:南京邮电大学仙林校区教3号楼\n文苑路9号(近南京财经大学仙林校区)
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=61.44644871598385;X-APPLE-REFERENCEFRAME=2;X-TITLE=南京邮电大学仙林校区教3号楼\\n文苑路9号(近南京财经大学仙林校区):geo:32.108513,118.922744"""
    },
    {
        "judge": "教4" in loc,
        "raw": r"""LOCATION:南京邮电大学仙林校区教4号楼\n文苑路9号(近南京财经大学仙林校区)
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=98.14109314594066;X-APPLE-REFERENCEFRAME=2;X-ADDRESS=文苑路9号(近南京财经大学仙林校区);X-TITLE=南京邮电大学仙林校区教4号楼:geo:32.109446,118.930161"""
    },
    {
        "judge":"教5" in loc,
        "raw": r"""LOCATION:南京邮电大学仙林校区教5号楼\n文苑路9号(近南京财经大学仙林校区)
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=52.98667907714844;X-APPLE-REFERENCEFRAME=0;X-TITLE=南京邮电大学仙林校区教5号楼\\n文苑路9号(近南京财经大学仙林校区):geo:32.110100,118.930272"""
    },
    {
        "judge": "学科楼" in loc,
        "raw": r"""LOCATION:南京邮电大学仙林校区计算机学科楼\n文苑路9号(近南京财经大学仙林校区)
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=22.22502269563359;X-APPLE-REFERENCEFRAME=2;X-TITLE=南京邮电大学仙林校区计算机学科楼\\n文苑路9号(近南京财经大学仙林校区):geo:32.114493,118.928096""",
    },
    {
        "judge": True,
        "raw": r"""LOCATION:南京邮电大学仙林校区\n文苑路9号(近南京财经大学仙林校区)
"""
    }
    ]

def AppleLoc(classroom):
    loc = ""
    for place in AppleMaps(classroom):
        if place["judge"]:
            loc = place["raw"]
            break
    return loc

# print(AppleLoc("教4-110"))
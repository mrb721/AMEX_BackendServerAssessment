from datetime import datetime, timezone, timedelta

# string utils
def formatURL(url, companyId):
    urlBreakdown = url.split('//')
    domain = ''

    # if format is consistent we get {domain_string} : {port}
    if len(urlBreakdown) == 2:
        domain = urlBreakdown[1]
    elif len(urlBreakdown) == 1:
        domain = urlBreakdown[0]
    else: 
        return None
    
    if domain.endswith('/'):
        domain = domain[:-1]

    return f'http://{domain}/companies/{companyId}'


# time utils - convert RFC3339 to datetime
def timeNow():
    return convertDatetimeToRFCFormat(datetime.now(timezone.utc))

def convertStringToDatetime(timestring):
    return datetime.fromisoformat(timestring) if timestring else None



def convertDatetimeToString(timestamp):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] if timestamp else None

def convertStringToRFCDatetime(timestring):
    # timestamp = datetime.fromisoformat("YYYY-MM-DDTHH:MM:SS.sssssssss")
    timestamp = convertStringToDatetime(timestring)
    return convertDatetimeToRFCFormat(timestamp) if timestamp else None

def convertDatetimeToRFCFormat(timestamp):
    # timestring = convertDatetimeToString(timestamp)
    # return datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
    timestring = convertDatetimeToString(timestamp)
    return datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc) if timestamp else None

def withinTimeLimit(nowTime, storeTime):
    nowTime = nowTime.replace(tzinfo=timezone.utc) if nowTime else None
    storeTime = storeTime.replace(tzinfo=timezone.utc) if storeTime else None
    return abs(nowTime - storeTime) < timedelta(hours=24) if nowTime and storeTime else nowTime and not storeTime
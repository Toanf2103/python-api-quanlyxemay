import datetime
def formatDate(ngay):
    formatType="%d-%m-%Y"
    return ngay.strftime(formatType)

def checkInvalid(rq,params):
    for param in params:
        if param not in rq:
            return False
    return True
def checkNull(rq,params):
    for param in params:
        if rq[param] is None:
            return False
    return True
#1.1
def init(drivers,drivernames,configmgr,drivermgr,kernel):
    sysctl = drivers[drivernames.index("sys")]
    display = drivers[drivernames.index("display")]
    display.printline(sysctl.uname())

#1.2
def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    display.printline("WalterOS")
    rows,columns = display.getdimmentions()
    net = True
    try:
        import requests
        import socket
    except:
        net = False
    display.printline("Display size: " + str(rows) + "x" + str(columns))
    if net:
        display.printline("Network is enabled")
    else:
        display.printline("Network is disabled")
    display.printline("Kernel build: " + kernel.build)
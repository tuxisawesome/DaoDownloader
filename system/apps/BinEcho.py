#1.1

def init(drivers, drivernames, configmgr, drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    if argv == "null":
        display.printline("")
    else:
        display.printline(argv)

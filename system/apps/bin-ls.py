#1.1

def init(drivers, drivernames, configmgr, drivermgr,kernel):
    sys = drivers[drivernames.index("sys")]
    display = drivers[drivernames.index("display")]
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    if argv == "null":
    
        x = "."
    else:
        x = argv
    y = sys.dir(x)
    if y == 1:
        display.printline("Directory does not exist")
    elif y == 255:
        display.printline("An unknown error occoured")
    else:
        display.printline("")
        display.printline("Directory listing for: " + x)
        for i in y:
            display.printline(i)
        display.printline("")

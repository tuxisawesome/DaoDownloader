#2.3
import sys

def init(display, verbosedrivers,configmgr,drivermgr,drivers,drivernames,kernel):
    # Add key paths to PATH variable
    init = configmgr.readconfig("init.cfg",kernel.configpath)

    if init == None:
        return
    sys.path.append("usr/bin")
    sys.path.append("usr/local/bin")  
    sys.path.append("bin") 


    # Load init programs
    initprogs = []
    initprognames = []
    for progs in init:
        progx = progs.split("=")
        keys = []
        vals = []
        for line in init:
            x = line.split("=")
            keys.append(x[0])
            vals.append(x[1])
        y = vals[keys.index(progx[0])]
        yx = y.split("/")
        drv = drivermgr.defload(yx[1],yx[0])
        if verbosedrivers:
            display.printline("**  Executing startup task " + progx[0] + " from " + y)
        try:
            execute_drv(drv,drivers,drivernames,configmgr,drivermgr,kernel)
        except:
            kernel.panic("The startup task has reached a critical error.")    

def execute_drv(drv,drivers,drivernames,configmgr,drivermgr,kernel):
    x = drv.init(drivers, drivernames, configmgr, drivermgr,kernel)
    if x == -1:
        execute_drv(drv,drivers,drivernames,configmgr,drivermgr,kernel)

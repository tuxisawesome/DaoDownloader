#1.0
def init(drivers,drivernames,configmgr,drivermgr,kernel):
    kernel_arguments = kernel.args
    display = drivers[drivernames.index("display")]
    display.printline("Kernel arguments:")
    if kernel_arguments == []:
        display.printline("None")
    else:
        for arg in kernel_arguments:
            display.printline(arg)
    return
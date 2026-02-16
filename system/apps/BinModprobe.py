#1.1
def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    if argv == "null":
        display.printline("Modprobe\nDao Coreutils\nLoad a kernel module interactively\nUsage: modprobe [name] [path in driverpath] [ImportName]\n       modprobe -c (Shows list of modules)\nExample: 'modprobe network core/net/ net-connect'\nWarning: This utility is only for advanced users and may break your system!")
    else:
        if argv == "-c":
            display.printline(kernel.configuration.modules.modulenames);return
        x = argv.split(" ")
        d = drivermgr.load(x[0],x[1])
        d.init(drivers,drivernames,configmgr,drivermgr,kernel)
        importname = x[2]
        kernel.configuration.modules.modules.append(d)
        kernel.configuration.modules.modulenames.append(importname)
        display.printline("Successfully loaded module " + importname)

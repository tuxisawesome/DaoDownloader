#1.1
def init(drivers, drivernames, configmgr, drivermgr,kernel):


    debug = True




    
    config = configmgr.readconfig("config.cfg")
    interactive = configmgr.getvalue(config, "interactive")
    display = drivers[drivernames.index("display")]
    if interactive == "0": interactive = False 
    else: interactive = True
    kernel_arguments = kernel.args
    if "interactive=false" in kernel_arguments: interactive = False
    if interactive:
        continues = True
        while continues:
            try:
                x = drivers[drivernames.index("input")].getinput("$ ")
                if x == "": continue

                if x == "exit":
                    return -1

                if x == "poweroff":
                    sys = drivers[drivernames.index("sys")]
                    display.printline("*   This system is going down for shutdown NOW!")
                    return
                
                
                if x == "env-reload":    
                    kernel.reload_env()
                    continue
                            
                if x == "help": 
                    display.printline("WalterOS Shell\nAvailable commands are:  env-reload poweroff")
                    continue
                try:
                    args = x.split(" ")
                    if len(args) > 1:
                        newargs = args
                        load = newargs.pop(0)
                        new=""
                        for arg in newargs:
                            new = new + arg + " "
                        new = new.strip()
                        newenv = configmgr.setvalue(configmgr.readconfig("env.cfg"), "argv", new)
                        configmgr.writeconfig("env.cfg",newenv)
                    else:
                        newenv = configmgr.setvalue(configmgr.readconfig("env.cfg"), "argv", "null")
                        configmgr.writeconfig("env.cfg",newenv)
                        load = x.split()[0]
                    try:
                        y = drivermgr.defload(load, "bin/")
                    except:
                        try:
                            y = drivermgr.defload(load, "usr/bin/")
                        except Exception as e:
                            display.printline("File not found! " + str(e))
                            continue
                except Exception as e:
                    display.printline("ERROR!")
                    print(e)
                    continue
                if debug:
                    x = y.init(drivers, drivernames, configmgr, drivermgr,kernel)
                    if x == "quit":
                        break
                    else:
                        continue
                else:
                    try:
                        x = y.init(drivers, drivernames, configmgr, drivermgr,kernel)
                        if x == "quit":
                            break
                        else:
                            continue
                    except:
                        display.printline("File may be corrupted!\nPlease check the arguments the file is taking.")
                        continue
            except Exception as e:
                display.printline(e)
                continue
            
    else:
        display.printline("!   Not an interactive shell, skipping...")


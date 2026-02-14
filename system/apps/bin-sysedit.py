#1.1
def init(drivers, drivernames, configmgr, drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    input = drivers[drivernames.index("input")]
    sysctl = drivers[drivernames.index("sys")]


    a = '['
    for arg in kernel.args:
        a += "'" + arg + "' "
    a += "]"
    a = a.strip()


    display.printline("System Settings")
    display.printline("Kernel arguments: " + a)
    display.printline("Please enter the setting file you want to edit.")
    display.printline("Type 'q' to quit.")
    display.printline("")
    files = sysctl.dir(kernel.configpath)
    count = 0
    for file in files:
        display.printline(str(count) + " - " + file.strip("\n"))
        count = count + 1
    x = input.getinput("? ")
    if x == "q" or x == "Q":
        return
    try:
        file = configmgr.readconfig(files[int(x)])
        stop = False
        while not stop:
            display.printline("Please select the entry you want to edit, or type 'w' to write or 'n' for new entry.")
            display.printline("Type 'q' to quit.")
            count = 0
            for entry in file:
                display.printline(str(count) + " - " + entry.strip("\n"))
                count = count + 1
            y = input.getinput("? ")
            if y == "w" or y == "W":
                break
            if y == "q" or y == "Q":
                return
            elif y == "n" or y == "N":
                key = input.getinput("Key of entry? ")
                value = input.getinput("Value of entry? ")
                file = configmgr.setvalue(file, key, value)
                continue
            try:
                specificentry = file[int(y)]
                key = specificentry.split("=")[0]
                value = specificentry.split("=")[1]
                display.printline("What would you like to do?")
                display.printline("1. Remove this entry")
                display.printline("2. Edit the value of this entry")
                z = input.getinput("[1, 2] ? ")
                if z == "1":
                    file = configmgr.remkey(file, key)
                    continue
                if z == "2":
                    aa = input.getinput("Value? ")
                    file = configmgr.setvalue(file, key, aa)
                    continue
                continue
            except:
                display.printline("An unknown error occoured.")
        display.printline("Writing changes to settings...")
        configmgr.writeconfig(sysctl.dir('etc/')[int(x)], file)
        display.printline("Changes written successfully.")
        display.printline("For edits to critical system files:\n      - Make sure to run 'bootsign' to re-sign the critical boot files.")
    except:
        display.printline("An unknown error occoured.")
    

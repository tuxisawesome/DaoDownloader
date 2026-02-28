#1.0

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    display.printline("Net-Connect")
    display.printline("Checking for a valid network driver...")
    try:
        network = drivers[drivernames.index("net-connect")]
    except:    
        display.printline("!   No network driver found. Please install a network driver to use this application.")
        return
    interactive = drivers[drivernames.index("input")]
    display.printline("Please enter the SSID of the network you wish to connect to:")
    ssid = interactive.getinput("SSID: ")
    password = interactive.getinput("Password (leave blank for open networks): ")
    display.printline("Attempting to connect to " + ssid + "...")
    network.connect(display,kernel,ssid, password)
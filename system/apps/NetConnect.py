#1.01

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    display.printline("Net-Connect")
    display.printline("Checking for a valid network driver...")
    try:
        network = drivers[drivernames.index("net-connect")]
    except:    
        display.printline("!   No network driver found. Please install a network driver to use this application.")
        return
    
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    if argv == "-c" or argv == "-C":
        interactive = drivers[drivernames.index("input")]
        display.printline("Please enter the SSID of the network you wish to connect to:")
        ssid = interactive.getinput("SSID: ")
        password = interactive.getinput("Password (leave blank for open networks): ")
        display.printline("Attempting to connect to " + ssid + "...")
        network.connect(display,kernel,ssid, password)
    elif argv == "-s" or argv == "-S":
        display.printline("Scanning for nearby networks...")
        ssidlist = network.scan_networks(kernel)
        if len(ssidlist) == 0:
            display.printline("No networks found.")
            return
        display.printline("Nearby Networks:")
        display.printline("================")
        for ssid in ssidlist:
            display.printline(ssid[0].decode("utf-8") + "  Strength: " + str(ssid[2]))
    elif argv == "-i" or argv == "-I":
        display.printline("Getting network information...")
        info = network.network_info(kernel)
        if info is None:
            display.printline("Not connected to a network.")
            return
        display.printline("IP Address: " + info[0])
        display.printline("Subnet Mask: " + info[1])
        display.printline("Gateway: " + info[2])
        display.printline("DNS: " + info[3])
    else:
        display.printline("Net-Connect")
        display.printline("Usage:")
        display.printline("net-connect -c    Connect to a network")
        display.printline("net-connect -s    Scan for nearby networks")
        display.printline("net-connect -i    Get network information")

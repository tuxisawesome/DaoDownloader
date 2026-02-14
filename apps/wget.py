#1.1

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    try:
        net = drivers[drivernames.index("net-connect")]
    except:
        display.printline("Please install a networking driver and then try again.")
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    if argv == "null":
        display.printline("Please provide a website argument.")
    else:
        x = argv.split(" ")
        if len(x) != 2:
            display.printline("Please provide two arguments: one website and one file to write to.")
            return
        website = x[0]
        file_to_patch = x[1]
        if not website.startswith("http:") and not website.startswith("https:"):
            display.printline("Please supply a valid schema. Example: http, https")
            return
        
        response_code, response_content = net.get_web_data(website,kernel)
        if response_code != 200:
            if response_code == -255:
                display.printline("Networking is not enabled.")
                return
            display.printline("Webpage responded with unknown response code: " + str(response_code))
            return
        with open(file_to_patch,"wb") as file:
            file.write(response_content)
            file.close()
        display.printline("File " + file_to_patch + " written " + str(len(response_content)) + " bytes.")
    

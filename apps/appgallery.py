#1.4
v = 1.4
repo_root = "https://raw.githubusercontent.com/tuxisawesome/DaoDownloader/refs/heads/main/"

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    net = drivers[drivernames.index("net-connect")]
    interactive = drivers[drivernames.index("input")]
    sysctl = drivers[drivernames.index("sys")]
    packagekit = drivers[drivernames.index("packagekit")]
    packagekit.configuration.repo_root = repo_root
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")


    display.printline("AppGallery " + str(v))
    

    if argv == "-R" or argv == "-r":
        display.printline("!!! REMOVAL MODE !!!")
        removal_mode = True
    else:
        removal_mode = False
    if argv == "-s" or argv == "-S":
        display.printline("** Syncing (updating) on-device applications")
        packagekit.sync_apps(display,net,sysctl,kernel)
        display.printline("** Please restart or run 'env-reload' to properly push changes.")
        return
    if argv == "-u" or argv == "-U":
        system_update(drivers,drivernames,configmgr,drivermgr,kernel)
        return

    website_root = repo_root
    response_code,response_data = net.get_web_data(website_root + "apps.txt",kernel)
    if response_code == -255:
        display.printline("No internet.")
        return
    if response_code == -1:
        display.printline("Server down.")
        return
    
    apps,appnames,vers,path = packagekit.read_repofile(str(response_data))

    display.printline("=== APPS ===")
    for appx in appnames:
        display.printline(appx + "  V:" + vers[appnames.index(appx)])
    app = interactive.getinput("Please enter the app or press q to quit: ")

    if app == "q" or app == "Q":
        return
    if app not in appnames:
        display.printline("This app does not exist.")
        return
    
    directory = path[appnames.index(app)]
    if not removal_mode:
        packagekit.install_app(website_root,apps,appnames,app,directory,display,net,kernel,sysctl,True)
    else:
        sysctl.rmfile(directory)
        display.printline("Application Removed.")












def system_update(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    net = drivers[drivernames.index("net-connect")]
    interactive = drivers[drivernames.index("input")]
    sysctl = drivers[drivernames.index("sys")]
    packagekit = drivers[drivernames.index("packagekit")]
    packagekit.configuration.repo_root = repo_root

    display.printline("System update")
    display.printline("Please type 'y' to confirm the update.")

    x = interactive.getinput("? ")
    if x == 'y' or x == "Y":
        x = packagekit.system_update_backend(repo_root + "system/",net,sysctl,kernel,display)
        if x == -255:
            display.printline("No internet.")
        if x == -1:
            display.printline("Server down.")
        if x == 0:
            display.printline("Please now run 'bootsign' in case any core system files changed.")



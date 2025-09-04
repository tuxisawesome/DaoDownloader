#1.0
v = 1.0
repo_root = "https://raw.githubusercontent.com/tuxisawesome/DaoDownloader/refs/heads/main/"

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    net = drivers[drivernames.index("net-connect")]
    interactive = drivers[drivernames.index("input")]
    sysctl = drivers[drivernames.index("sys")]
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")


    display.printline("AppGallery " + str(v))


    if argv == "-R" or argv == "-r":
        display.printline("!!! REMOVAL MODE !!!")
        removal_mode = True
    else:
        removal_mode = False
    if argv == "-s" or argv == "-S":
        display.printline("** Syncing (updating) on-device applications")
        sync_apps(display,net,sysctl,kernel)
        display.printline("** Please restart or run 'env-reload' to properly push changes.")
        return
    

    website_root = repo_root
    response_code,response_data = net.get_web_data(website_root + "apps.txt",kernel)
    if response_code == -255:
        display.printline("No internet.")
        return
    if response_code == -1:
        display.printline("Server down.")
        return
    
    apps,appnames,vers,path = read_repofile(str(response_data))

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
        install_app(website_root,apps,appnames,app,directory,display,net,kernel)
    else:
        sysctl.rmfile(directory + apps[appnames.index(app)])
        display.printline("Application Removed.")


def download_file(website,directory,filename,net,kernel):
    if not website.startswith("http:") and not website.startswith("https:"):
        return -2
    response_code, response_content = net.get_web_data(website,kernel)
    if response_code != 200:
        if response_code == -255:
            return -255
        elif response_code == 404:
            return 404
        return -1
    with open(directory + "/" + filename, "wb") as file:
        file.write(response_content)
        file.close()
    return 0


def read_repofile(file):
    file = file.split("'")[1]
    lines = file.split("\\n")
    apps = []
    appnames = []
    vers=[]
    path=[]
    if lines[0] == ";;repofile":
        pass
    else:
        return None
    for line in lines:
        if line.startswith("#") or line.startswith("//") or line == "" or line.startswith(";;"):
            continue
        f = line.split("=")
        appnames.append(f[0])
        apps.append(f[1])
        vers.append(f[2])
        path.append(f[3])
    return apps,appnames,vers,path


def install_app(website_root,apps,appnames,app,directory,display,net,kernel):
    x = download_file(website_root + "apps/" + apps[appnames.index(app)], directory, apps[appnames.index(app)],net,kernel)
    if x == 404:
        display.printline("This application does not exist, or the server is down.")
        return
    elif x == -255:
        display.printline("The network is not connected.")
    elif x == -1:
        display.printline("The system encounterred a strange error code.")
    elif x == -2:
        display.printline("The repository name is incorrect.")
    else:
        display.printline("The application " + app + " was installed/updated successfully.")

def sync_apps(display,net,sysctl,kernel):
    website_root = repo_root
    response_code,response_data = net.get_web_data(website_root + "apps.txt",kernel)
    if response_code == -255:
        display.printline("No internet.")
        return
    if response_code == -1:
        display.printline("Server down.")
        return
    apps,appnames,vers,path = read_repofile(str(response_data))
    for paths in path:
            for appe in apps:
                if appe in sysctl.dir(paths):
                    with open(paths + appe, "r") as txt:
                        if float(txt.readlines()[0][1:]) <= float(vers[apps.index(appe)]):
                            continue
                        txt.close()
                    directory = path[apps.index(appe)]
                    install_app(website_root,apps,appnames,appnames[apps.index(appe)],directory,display,net,kernel)


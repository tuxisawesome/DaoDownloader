#1.5
class configuration:
    repo_root = "https://raw.githubusercontent.com/tuxisawesome/DaoDownloader/refs/heads/main/"


def init(driver,drivernames,configmgr,drivermgr,kernel):
    pass


def download_file(website,directoryfile,net,kernel,sys,createdirectory=False):
    if not website.startswith("http:") and not website.startswith("https:"):
        return -2
    response_code, response_content = net.get_web_data(website,kernel)
    if response_code != 200:
        if response_code == -255:
            return -255
        elif response_code == 404:
            return 404
        return -1
    directory = ""
    p = directoryfile.split("/")[:-1]
    for name in p: directory = directory + name + "/"
    x = sys.dir(directory) # Check if directory exists
    if x == 1:
        # Create directory
        sys.makedirs(directory)
    with open(directoryfile, "wb") as file:
        file.write(response_content)
        file.close()
    return 0


def install_app(website_root,apps,appnames,app,directory,display,net,kernel,sys,createdirectory=False):
    x = download_file(website_root + "apps/" + apps[appnames.index(app)], directory,net,kernel,sys,createdirectory)
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

def system_update_backend(website_root,net,sysctl,kernel,display):
    response_code,response_data = net.get_web_data(website_root + "apps.txt",kernel)
    if response_code == -255:
        return -255
    if response_code == -1:
        return -1
    apps,appnames,vers,path = read_repofile(str(response_data))
    for paths in path:
            pathsx = remove_trailing_filename(paths)
            for appe in apps:
                if appe in sysctl.dir(pathsx):
                    with open(paths, "r") as txt:
                        if float(txt.readlines()[0][1:]) >= float(vers[apps.index(appe)]):
                            continue # The version of the app is the same or greater than the one on the server
                        txt.close()
                    directory = path[apps.index(appe)]
                    if appnames[apps.index(appe)] == "kernel":
                        display.printline("** Installing new kernel to replace kernel version " + kernel.build)
                        display.printline("** Please make sure to restart in order for the new kernel to take effect.")
                    install_app(website_root,apps,appnames,appnames[apps.index(appe)],directory,display,net,kernel,sysctl,True)

def remove_trailing_filename(path=""):
    x = path.split("/")
    x.pop()
    if x == []:
        return path
    y = ""
    for thing in x:
        y = y + thing + "/"
    return y


def sync_apps(display,net,sysctl,kernel):
    website_root = configuration.repo_root
    response_code,response_data = net.get_web_data(website_root + "apps.txt",kernel)
    if response_code == -255:
        display.printline("No internet.")
        return
    if response_code == -1:
        display.printline("Server down.")
        return
    apps,appnames,vers,path = read_repofile(str(response_data))
    found_updates = False
    for paths in path:
            pathsx = remove_trailing_filename(paths)
            for appe in apps:
                if appe in sysctl.dir(pathsx):
                    with open(pathsx + appe, "r") as txt:
                        if float(txt.readlines()[0][1:]) >= float(vers[apps.index(appe)]):
                            continue # The version of the app is the same or greater than the one on the server
                        txt.close()
                    
                    directory = path[apps.index(appe)]
                    install_app(website_root,apps,appnames,appnames[apps.index(appe)],directory,display,net,kernel,sysctl,False)
                    found_updates = True


def read_repofile(file):
    file = file.split("'")[1]
    lines = file.split("\\n")
    apps = []
    appnames = []
    vers=[]
    path=[]
    if lines[0].startswith(";;repofile"):
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


def install(app,website_root,net,sysctl,kernel,display,removal=False):
    response_code,response_data = net.get_web_data(website_root + "apps.txt",kernel)
    if response_code == -255:
        return -255
    if response_code == -1:
        return -1
    
    apps,appnames,vers,path = read_repofile(str(response_data))
    if app not in appnames:
        return -404
    directory = path[appnames.index(app)]
    if not removal:
        install_app(website_root,apps,appnames,app,directory,display,net,kernel,sysctl,False)
        return 0
    else:
        sysctl.rmfile(directory + apps[appnames.index(app)])
        return 0    
    

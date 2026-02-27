#4.4
bd="4.4" # Build number

GLOBAL_SIP = False

import sys


def boot(args): kernel.panic("\nThe kernel is not directly bootable\nPlease use a seperate bootloader to load the kernel.")

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    display.printline("The kernel is not an application.")




def main(args):
        vdrivers = False
        if len(args) >= 1:
            for arg in args:
                arg = arg.lower().split("=")
                if arg[0] == "configpath":
                    kernel.configpath = arg[1];continue
                if arg[0] == "driverpath":
                    kernel.driverpath = arg[1];continue
                if arg[0] == "verbosedrivers" and arg[1] == "true":
                    vdrivers = True;continue
                if arg[0] == "verbosedrivers" and arg[1] == "false":
                    vdrivers = False;continue
        
        kernel.args = args
        mods = configmgr.readconfig("modules.cfg",kernel.configpath)

        config = configmgr.readconfig("config.cfg",kernel.configpath)

        # Establish constants
        ver = configmgr.getvalue(config, "version")
        verbosedrivers = configmgr.getvalue(config, "verbosedrivers")
        if vdrivers == False:
            if verbosedrivers == "0": verbosedrivers = False; kernel.verbosedrivers = False
            else: verbosedrivers = True;kernel.verbosedrivers = True
        else: verbosedrivers = True;kernel.verbosedrivers = True


        # Loads display module
        try:
            x = configmgr.getvalue(mods, "display")
            y = x.split("/")
            display = drivermgr.load(y[1],y[0])
        except:
            display = kernel.configuration.modules.display # Fallback builtin display driver
        

        display.printline("Dao " + ver + " is starting up!")
        try:    # Loads other modules into drivers,drivernames
            drivers,drivernames = load_modules(display,mods,verbosedrivers)
            kernel.configuration.modules.modules = drivers
            kernel.configuration.modules.modulenames = drivernames
        except:
            drivers = kernel.configuration.modules.modules  # Fallback builtin modules
            drivernames = kernel.configuration.modules.modulenames # Fallback builtin modulenames

        sys.path.insert(1, 'sbin/')
        try:# Load init server
            import init as start
        except:
            kernel.panic("Unable to find init at '/sbin/init")
        try:# Jump to init server, needs a lot of arguments to have the proper environment to execute programs
            display.printline("*   Loading init at /sbin/init")
            start.init(display,verbosedrivers,configmgr,drivermgr,kernel.configuration.modules.modules,kernel.configuration.modules.modulenames,kernel) 
        except:
            kernel.panic("init does not have init function or other error occoured")
        '''
        You can also use the default __import__ function as
        module = __import__(custom)
        '''



def load_modules(display,mods,verbosedrivers):
    # load other modules
    drivers = []
    drivernames = []
    for mod in mods:
        modx = mod.split("=")
        keys = []
        vals = []
        for line in mods:
            x = line.split("=")
            keys.append(x[0]) # Appends the name
            vals.append(x[1]) # Appends the path
        y = vals[keys.index(modx[0])].strip("\n") # The path x[1]
        yx = y.split("/") # Splits the path by the /shes
        drivername = yx.pop(-1)        
        totallines = ""
        for d in yx:
            totallines = totallines + d + "/"
        totallines.strip("/")


        drv = drivermgr.load(drivername,totallines) #Attempts to load the driver by yx[-1] (module name) with path yx[0]
        drivernames.append(modx[0])
        drivers.append(drv)
        drv.init(drivers, drivernames, configmgr, drivermgr, kernel)
        if verbosedrivers:
            display.printline("*   Loaded module " + modx[0] + " from " + y)
    # find drivers like this: drivers[drivernames.index("[name]")]
    display.printline("*   Drivers Loaded Successfully")
    return drivers,drivernames




class kernel:
    build=bd
    args=[]
    configpath="etc/"
    driverpath = "lib/"    

    sip=GLOBAL_SIP # Enables system integrity protection

    class configuration:
        defconfig = ["version=1.0","verbosedrivers=1"]# Fallback for config.cfg file
        definitconfig = ["bp=bin/basicprogram"]# Fallback for init.cfg file
        defaults = {"config.cfg": defconfig,"init.cfg": definitconfig}# Definitions for default files
        
        class modules: # Default modules
            class display:
                def printline(str):
                    print(str)
            modules = [display] # Contains a reference to every default module in a list
            modulenames = ["display"]   # Human-readable name for each module in the list



    verbosedrivers=False
    def panic(message="Unknown"):   # Executes a kernel panic, halting code execution
        if "panic=false" in kernel.args:
            return
        try:
            print("The kernel has reached an unrecoverable error.")
            print("Please force restart the computer.")
            print("Error: " + message)
            while True:
                continue
        except:
            kernel.panic(message)


    def reload_env():
        good_modules = ["sys","requests","certifi","charset_normalizer","idna","urllib3","socket","encodings","__future__","collections","json","encodings.idna","idna","logging","re","typing","warnings","zlib","contextlib","http","email","random","datetime","urllib","functools","math","types","ipaddress","calendar","base64","binascii","string","quopri","enum","hashlib","hmac","select","selectors","ssl","zstandard","queue","threading","importlib","csv","pathlib","zipfile","operator","textwrap","copy","unicodedata","dis","inspect","platform","mimetypes","tempfile","weakref","atexit","errno","array","locale","fnmatch","ntpath","opcode","stringprep",
                        "decimal","platform"]

        s = drivermgr.basicload("sys")
        x = s.modules

        try:
            
            for mod in x:
                if mod in good_modules: continue
                if kernel.verbosedrivers: print("*   '" + mod + "' is reloaded.")
                del s.modules[mod]
                del mod
                            
        except:
            kernel.reload_env()

































































































# Configmgr
class configmgr:
    def readconfig(file,path=kernel.configpath):
        try:
            with open(path + file, "r") as f:
                x = f.readlines()
                y = []
                for line in x:
                    if line.startswith("#") or line.startswith("//") or line == "":
                        continue
                    else:
                        y.append(line.strip("\n"))
                return y
        except:
            if file in kernel.configuration.defaults.keys():
                return kernel.configuration.defaults.get(file,None)
            return None

    def writeconfig(file, config,path=kernel.configpath):
        with open(path + file, "w") as f:
            f.write("# Autogenerated by writeconfig\n")
            for line in config:
                if not line.endswith("\n"):
                    f.write(line + "\n")
                else: f.write(line)
            f.close()
        
    def getvalue(config, key):
        keys = []
        vals = []
        for line in config:
            x = line.split("=")
            keys.append(x[0])
            vals.append(x[1])
        return vals[keys.index(key)].strip("\n")

    def getkeys(config):
        keys = []
        vals = []
        for line in config:
            x = line.split("=")
            keys.append(x[0].strip("\n"))
            vals.append(x[1])
        return keys

    def getkey(config, value):
        keys = []
        vals = []
        for line in config:
            x = line.split("=")
            keys.append(x[0])
            vals.append(x[1])
        return keys[vals.index(value)].strip("\n")

    def setvalue(config, key, value):
        keys = []
        vals = []
        for line in config:
            x = line.split("=")
            keys.append(x[0])
            vals.append(x[1])
        try:
            vals[keys.index(key)] = value
        except ValueError or IndexError:
            keys.append(key)
            vals.append(value)
        newconfig = []
        for z in keys:
            newconfig.append(z + "=" + vals[keys.index(z)])

        return newconfig


    def remkey(config, key):
        keys = []
        vals = []
        for line in config:
            x = line.split("=")
            keys.append(x[0])
            vals.append(x[1])
        try:
            vals.pop(keys.index(key))
            keys.pop(keys.index(key))
        except ValueError:
            pass
        newconfig = []
        for z in keys:
            newconfig.append(z + "=" + vals[keys.index(z)])

        return newconfig



#Drivermgr
class drivermgr:
    def load(name, path_in_driverpath): # Example: name = "print", path in driverpath = core/
        try:
            sys.path.append(kernel.driverpath + path_in_driverpath)   
        except:
            kernel.panic("Driver path incorrect or does not exist: " + kernel.driverpath + path_in_driverpath)
        try: 
            x = __import__(name.strip("\n"))
        except:
            kernel.panic("\nDriver " + name.strip("\n") + " does not exist.\n" + "Driver path incorrect or does not exist: " + kernel.driverpath + path_in_driverpath)
            kernel.panic("Driver " + name.strip("\n") + " does not exist.")
        return x

    def defload(name, path):
        sys.path.append(path + "/") 
        d = __import__(name.strip("\n"))
        return d
    
    def basicload(name):
        return __import__(name.strip("\n"))

    def unload(name):
        del name



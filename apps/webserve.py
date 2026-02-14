#1.1


def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    try:
        serve = drivers[drivernames.index("net-serve")]
    except:
        display.printline("Please install 'server' networking drivers and then try again.")
    if not serve.validcheck(kernel):
        display.printline("No internet. No server.")
        return
    socket = serve.socket(kernel)
    if socket == None:
        display.printline("No internet. No server.")
        return
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    display.printline("Listening on " + str(addr))

    # Arguments
    list_of_addresses = ['/light/on','/light/off', '/']
    list_of_html = [b"Light on",b"Light off", b'Banana']
    fourohfour = b"<html><head><title>404</title></head><body><h1>404 Error</h1><p>The requested resource could not be found.</p></body></html>"


    # Listen for connections
    while True:
        try:
            cl, addr = s.accept()
            request = cl.recv(1024)
            request = str(request)

            
            exit = request.find('/exit')
            if exit == 6:
                cl.close()
                return
            html = ""
            found = False


            for address in list_of_addresses:
                if request.startswith("b'GET " + address + " H") or request.startswith("b'GET " + address + "/ H"):
                    html = list_of_html[list_of_addresses.index(address)]
                    found = True
            if found == False:
                html = fourohfour
            response = html

            cl.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()

        except OSError:
            cl.close()

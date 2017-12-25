import ctypes
import socket
import struct

def get_macaddress(host):
    """ Returns the MAC address of a network host, requires >= WIN2K. """
    try:
        SendARP = ctypes.windll.Iphlpapi.SendARP
    except:
        raise NotImplementedError('Usage only on Windows 2000 and above')
    if host == '127.0.0.1' or host.lower() == 'localhost':
        host = socket.gethostname()
    try:
        inetaddr = ctypes.windll.wsock32.inet_addr(host)
        if inetaddr in (0, -1):
            raise Exception
    except:
        hostip = socket.gethostbyname(host)
        inetaddr = ctypes.windll.wsock32.inet_addr(hostip)
    buffer = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(buffer))
    if SendARP(inetaddr, 0, ctypes.byref(buffer), ctypes.byref(addlen)) != 0:
        raise WindowsError('Retreival of mac address(%s) - failed' % host)
    macaddr = ''
    for intval in struct.unpack('BBBBBB', buffer):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        macaddr = ''.join([macaddr, hex(intval).replace(replacestr, '')])
        macaddr2 = ':'.join((macaddr)[i:i+2] for i in range(0, 12, 2))
    return macaddr2.upper()

if __name__ == '__main__':
    print ('[+] 1 -- A MAC ADDRESS')
    print ('[+] 2 -- Range of MAC ADDRESS')
    print ('Note : Must get MAC ADDRESS from local Network')
    order = raw_input('Choice a number : ')
    choice = ["1","2"]
    while not order in choice:
        print ('Please choice 1 or 2, Try again')
        order = raw_input('Choice a number : ')
        
    while True:
        if order == "1":
            print ('Enter a ip address')
            ipaddress = raw_input('IP ADDRESS : ')
            while ipaddress == "":
                ipaddress = raw_input('IP ADDRESS : ')
            try:
                routeripaddress = '{}.{}.{}.1'.format(ipaddress.split('.')[0],ipaddress.split('.')[1],ipaddress.split('.')[2])
                whatisroutermacone = get_macaddress(routeripaddress)
                macaddressgotone = get_macaddress(ipaddress)
                if ipaddress == routeripaddress:
                    print ('[+] {} MAC ADDRESS >> {}'.format(ipaddress,whatisroutermacone))
                elif macaddressgotone == whatisroutermacone:
                    print('[+] {} ROUTER MAC ADDRESS >> {}'.format(routeripaddress,whatisroutermacone))
                    print ('[+] {} MAC ADDRESS IS NOT FOUND'.format(ipaddress))
                else:
                    print('[+] {} ROUTER MAC ADDRESS >> {}'.format(routeripaddress,whatisroutermacone))
                    print ('[+] {} MAC ADDRESS IS {}'.format(ipaddress,macaddressgotone))
            except:
                print ('ERROR, Try Again')
                
        elif order == "2":
            print ('Enter a Network ID and range IP from x to x .. EX: 192.168.1.0 from 50 to 100')
            rangeipaddress = raw_input('NETWORK ID : ')
            splitinput = rangeipaddress.split(" ")
            cheackinput = ["from","to"]
            while rangeipaddress == "":
                print ('Try agaig EX: 192.168.1.0 from 50 to 100')
                rangeipaddress = raw_input('NETWORK ID : ')
            try:
                networkid = '{}.{}.{}.'.format(splitinput[0].split('.')[0],splitinput[0].split('.')[1],splitinput[0].split('.')[2])
                fromrange = int(splitinput[2])
                finishedrange = int(splitinput[4])+1
                whatisroutermac = get_macaddress('{}1'.format(networkid))
                print('[+] {}1 ROUTER MAC ADDRESS IS : {}'.format(networkid,whatisroutermac))
                for networkrangeid in range(fromrange,finishedrange):
                    ipaddressforgetmac = '{}{}'.format(networkid,networkrangeid)
                    try:
                        macaddressgot = get_macaddress(ipaddressforgetmac)
                        if macaddressgot == whatisroutermac:
                            print ('[+] {} MAC ADDRESS IS NOT FOUND'.format(ipaddressforgetmac))
                        else:
                            print ('[+] {} MAC ADDRESS >> {}'.format(ipaddressforgetmac,macaddressgot))
                    except:
                        print ('[+] {} MAC ADDRESS IS NOT FOUND'.format(ipaddressforgetmac))
            except:
                print ('ERROR, Try Again')
                
                








            

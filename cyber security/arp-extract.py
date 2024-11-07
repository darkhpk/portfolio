import os

for device in os.popen('arp -a'):
    # example output: xxxx (192.168.1.254) at xx:xx:xx:xx:xx:xx [ether] on wlp..
    _, ip, _, phy, _ = device.split(maxsplit=4)
    # remove the paranthesis around the ip address
    ip = ip.strip('()')
    print(ip, phy)
from scapy.all import sniff, get_if_list

def packet_callback(packet):
    print(f"Packet: {packet.summary()}")

if __name__ == "__main__":
    interface = "wlan0"
    
    print(get_if_list())
    sniff(iface=interface, prn=packet_callback, count=10)
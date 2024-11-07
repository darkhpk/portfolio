import time
from ping3 import ping

def ping_remote_host(host):
    try:
        response_time = ping(host, timeout=1)
        if response_time is None:
            print(f"{host} is unreachable.")
        else:
            print(f"Ping to {host}: {response_time * 1000:.2f} ms")
    except Exception as e:
        print(f"Ping to {host} failed: {e}")

if __name__ == "__main__":
    remote_ip = "192.168.1.116"  # Replace with your remote IP address

    while True:
        ping_remote_host(remote_ip)
        time.sleep(5)  # Delay for 5 seconds between pings

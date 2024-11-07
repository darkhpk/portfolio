# You need to download and install Tor
# configure Tor to allow control access (torrc)
# using command tor --hash-password "password"

import requests
from stem import Signal
from stem.control import Controller

def get_current_ip():
    """Get the current public IP address."""
    try:
        response = requests.get("http://icanhazip.com")
        return response.text.strip()
    except requests.RequestException:
        return "Unable to get IP"

def change_ip():
    """Request a new IP address from Tor."""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")  # Use your password here
        controller.signal(Signal.NEWNYM)

def main():
    print(f"Current IP: {get_current_ip()}")
    
    change_ip()
    
    # Wait a bit for the IP to change
    import time
    time.sleep(5)
    
    print(f"New IP: {get_current_ip()}")

if __name__ == "__main__":
    main()

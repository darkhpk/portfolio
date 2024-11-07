from scapy.all import ARP, Ether, sniff, conf
import threading, requests
import time
from collections import defaultdict
from plyer import notification

class ARPMonitor:
    def __init__(self):
        # Dictionary to store IP-to-MAC mapping
        self.arp_table = defaultdict(set)
        # List to store detected attacks
        self.alerts = []
        # Lock for thread-safe operations on arp_table
        self.lock = threading.Lock()
        # Notification method and Slack webhook URL, default to desktop notification
        self.notification_method = "desktop"
        self.slack_webhook_url = None

    def detect_arp_spoofing(self, packet):
        if packet.haslayer(ARP):
            # Check if it's an ARP response (is-at packet)
            if packet[ARP].op == 2:
                src_ip = packet[ARP].psrc
                src_mac = packet[ARP].hwsrc

                with self.lock:
                    # If the IP is already in the table and the MAC address is different, alert
                    if src_mac not in self.arp_table[src_ip]:
                        if self.arp_table[src_ip]:
                            alert_message = f"[!] ARP Spoofing Detected: {src_ip} is being spoofed! MAC {src_mac}"
                            self.alerts.append(alert_message)
                            print(alert_message)
                            # Send the alert using the chosen notification method
                            self.send_alert(alert_message)

                        # Update the ARP table
                        self.arp_table[src_ip].add(src_mac)

    def send_alert(self, alert_message):
        """
        Send an alert using the specified notification method.
        
        Parameters:
        - alert_message (str): The message to be sent in the alert.
        """
        if self.notification_method == "desktop":
            # Send desktop notification
            notification.notify(
                title="ARP Monitor Alert",
                message=alert_message,
                app_name="ARP Monitor",
                timeout=10  # Notification duration in seconds
            )
            print("[*] Desktop notification sent.")
            
        elif self.notification_method == "slack":
            # Send Slack notification
            if self.slack_webhook_url is None:
                print("[!] Slack webhook URL is required for Slack notifications.")
                return

            slack_data = {
                "text": alert_message
            }
            response = requests.post(self.slack_webhook_url, json=slack_data)
            if response.status_code == 200:
                print("[*] Slack notification sent.")
            else:
                print(f"[!] Failed to send Slack notification. Status code: {response.status_code}")
        else:
            print(f"[!] Unsupported notification method: {self.notification_method}")

    def start_sniffing(self):
        print("[*] Starting ARP monitor...")
        # Start sniffing ARP packets on the network
        sniff(store=False, prn=self.detect_arp_spoofing, filter="arp", iface=conf.iface)

    def get_alerts(self):
        return self.alerts

    def set_notification_method(self, method, slack_webhook_url=None):
        """
        Set the notification method and optionally the Slack webhook URL.
        
        Parameters:
        - method (str): The notification method to use. Either 'desktop' or 'slack'.
        - slack_webhook_url (str): The Slack webhook URL for sending Slack notifications. Required if method is 'slack'.
        """
        self.notification_method = method
        if method == "slack":
            self.slack_webhook_url = slack_webhook_url
            if not slack_webhook_url:
                print("[!] Warning: Slack webhook URL is not provided. No alerts will be sent to Slack.")

# Example usage
if __name__ == "__main__":
    arp_monitor = ARPMonitor()
    
    # Set notification method (choose either 'desktop' or 'slack')
    # For desktop notification
    arp_monitor.set_notification_method("desktop")

    # For Slack notification (replace 'your-slack-webhook-url' with the actual Slack webhook URL)
    # arp_monitor.set_notification_method("slack", slack_webhook_url="your-slack-webhook-url")

    # Run ARP monitor in a separate thread
    arp_thread = threading.Thread(target=arp_monitor.start_sniffing)
    arp_thread.start()

    try:
        while True:
            # Check for alerts every 10 seconds
            time.sleep(10)
            alerts = arp_monitor.get_alerts()
            if alerts:
                for alert in alerts:
                    print(alert)
                # Clear alerts after printing
                with arp_monitor.lock:
                    arp_monitor.alerts.clear()

    except KeyboardInterrupt:
        print("\n[!] Stopping ARP monitor.")
        arp_thread.join()

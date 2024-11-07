from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PIL import Image
import psutil
from scapy.all import sniff, ARP
import GPUtil
import threading
import time
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from collections import deque
import datetime

# Mock function to check certification status (for illustration purposes)
def check_certification_status(process_name):
    certified_processes = ["System", "svchost.exe", "explorer.exe", "google.exe"]
    return "Certified" if process_name in certified_processes else "Non-Certified"

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes) < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"  # In case of extremely large values


class SegmentMonitor(QWidget):
    # Signal to indicate a click on the segment name label
    segment_clicked = pyqtSignal(str)

    def __init__(self, name, max_length=60):
        super().__init__()
        self.name = name
        self.max_length = max_length  # Maximum data points for the graph

        # Data storage for the graph
        self.data = deque([0] * max_length, maxlen=max_length)
        self.time_stamps = deque([datetime.datetime.now()] * max_length, maxlen=max_length)

        # Initialize GUI elements
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Segment name label with clickable property
        self.name_label = QLabel(f"{self.name}: ")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("font-size: 14px; color: blue; text-decoration: underline; cursor: pointer;")
        self.name_label.mousePressEvent = self.on_name_click  # Connect click event
        layout.addWidget(self.name_label)

        # Usage percentage label
        self.usage_label = QLabel("0%")
        self.usage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usage_label.setStyleSheet("font-size: 12px;")  # Set font size for better readability
        layout.addWidget(self.usage_label)

        # Create matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Initial plot setup
        self.ax.set_title(f"{self.name} Usage")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Usage (%)")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.line, = self.ax.plot(self.time_stamps, self.data, 'g-')

        # Add the annotation (tooltip)
        self.annotation = self.ax.annotate(
            "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        self.annotation.set_visible(False)

        # Connect the motion event
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

        self.setLayout(layout)
        self.setMinimumSize(300, 200)  # Minimum size for each segment widget

    def update_usage(self, usage):
        # Update the usage label and the graph data
        self.usage_label.setText(f"{usage:.2f}%")
        self.data.append(usage)
        self.time_stamps.append(datetime.datetime.now())
        self.update_graph()

    def update_graph(self):
        # Update the graph with new data
        self.line.set_data(self.time_stamps, self.data)
        self.ax.set_xlim([self.time_stamps[0], self.time_stamps[-1]])
        self.ax.set_ylim([0, 100])
        self.canvas.draw()

    def on_hover(self, event):
        # Check if the mouse is over the line
        if event.inaxes == self.ax:
            # Find the closest data point
            closest_index = self.find_closest_index(event.xdata)
            if closest_index is not None:
                x = self.time_stamps[closest_index]
                y = self.data[closest_index]

                # Update and show the annotation
                self.annotation.xy = (x, y)
                self.annotation.set_text(f"{y:.2f}% at {x.strftime('%H:%M:%S')}")
                self.annotation.set_visible(True)
                self.canvas.draw()
            else:
                self.annotation.set_visible(False)
                self.canvas.draw()

    def find_closest_index(self, x_value):
        # Find the index of the closest timestamp to the given x_value
        if len(self.time_stamps) > 0:
            closest_index = min(range(len(self.time_stamps)), key=lambda i: abs(mdates.date2num(self.time_stamps[i]) - x_value))
            return closest_index
        return None

    def on_name_click(self, event):
        # Emit the signal with the segment name when clicked
        self.segment_clicked.emit(self.name)

class ResourceDetailsPopup(QWidget):
    def __init__(self, segment_name):
        super().__init__()
        self.segment_name = segment_name
        self.setWindowTitle(f"{segment_name} Usage Details")
        self.setGeometry(100, 100, 800, 400)

        # Create table for process details
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Program Name", "Certification", "Percentage Usage", "Usage", "Installation Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Dictionary to keep track of the previous network I/O counters for calculating bandwidth
        self.previous_net_io = {}

        # Timer for real-time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(2000)  # Update every 2 seconds

        # Populate the table initially
        self.populate_table()

    def populate_table(self):
        processes = []
        if self.segment_name == "CPU":
            processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'exe']), key=lambda p: p.info['cpu_percent'], reverse=True)
        elif self.segment_name == "Memory":
            processes = sorted(psutil.process_iter(['pid', 'name', 'memory_percent', 'exe']), key=lambda p: p.info['memory_percent'], reverse=True)
        elif self.segment_name == "Disk":
            processes = sorted(psutil.process_iter(['pid', 'name', 'io_counters', 'exe']), key=lambda p: self.get_disk_usage(p), reverse=True)
        elif self.segment_name == "Network":
            # Calculate bandwidth usage by getting the difference in bytes over the update interval
            processes = sorted(psutil.process_iter(['pid', 'name', 'io_counters', 'exe']), key=lambda p: self.get_network_bandwidth(p), reverse=True)
        elif self.segment_name == "GPU":
            processes = sorted(GPUtil.getGPUs(), key=lambda gpu: gpu.memoryUsed, reverse=True)

        self.table.setRowCount(len(processes))

        for row, proc in enumerate(processes):
            try:
                if self.segment_name == "GPU":
                    name = proc.name
                    path = "N/A"
                    certification = "N/A"
                    percent_usage = (proc.memoryUsed / proc.memoryTotal) * 100
                    usage_bytes = proc.memoryUsed * 1024 * 1024  # Convert MB to Bytes
                    usage_str = format_size(usage_bytes)
                else:
                    name = proc.info['name']
                    path = proc.info['exe'] if proc.info['exe'] else "N/A"
                    certification = check_certification_status(name)

                    # Calculate usage and display appropriately
                    if self.segment_name == "CPU":
                        percent_usage = proc.info['cpu_percent']
                        usage_str = "N/A"  # No direct usage values for CPU
                    elif self.segment_name == "Memory":
                        percent_usage = proc.info['memory_percent']
                        usage_bytes = proc.memory_info().rss
                        usage_str = format_size(usage_bytes)
                    elif self.segment_name == "Disk":
                        io_counters = proc.info['io_counters']
                        if io_counters:
                            percent_usage = (io_counters.read_bytes + io_counters.write_bytes) / psutil.disk_io_counters().write_bytes * 100
                            usage_bytes = io_counters.read_bytes + io_counters.write_bytes
                            usage_str = format_size(usage_bytes)
                        else:
                            percent_usage = 0
                            usage_str = format_size(0)
                    elif self.segment_name == "Network":
                        # Calculate the network bandwidth usage per second
                        net_io_counters = proc.info['io_counters']
                        if net_io_counters:
                            previous_net_io = self.previous_net_io.get(proc.info['pid'], (0, 0))
                            bytes_sent_per_sec = net_io_counters.bytes_sent - previous_net_io[0]
                            bytes_recv_per_sec = net_io_counters.bytes_recv - previous_net_io[1]
                            self.previous_net_io[proc.info['pid']] = (net_io_counters.bytes_sent, net_io_counters.bytes_recv)

                            percent_usage = (bytes_sent_per_sec + bytes_recv_per_sec) / 1024  # Convert to KBps for percentage
                            usage_str = f"{format_size(bytes_sent_per_sec)}/s sent, {format_size(bytes_recv_per_sec)}/s recv"
                        else:
                            percent_usage = 0
                            usage_str = "N/A"

                self.table.setItem(row, 0, QTableWidgetItem(name))
                self.table.setItem(row, 1, QTableWidgetItem(certification))
                self.table.setItem(row, 2, QTableWidgetItem(f"{percent_usage:.2f}%"))
                self.table.setItem(row, 3, QTableWidgetItem(usage_str))
                self.table.setItem(row, 4, QTableWidgetItem(path))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                continue


    def update_table(self):
        """Refresh the table data."""
        self.populate_table()

    def get_disk_usage(self, proc):
        try:
            io_counters = proc.info['io_counters']
            if io_counters:
                return io_counters.read_bytes + io_counters.write_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return 0
        return 0

    def get_network_bandwidth(self, proc):
        try:
            net_io_counters = proc.info['io_counters']
            previous_net_io = self.previous_net_io.get(proc.info['pid'], (0, 0))
            bytes_sent_per_sec = net_io_counters.bytes_sent - previous_net_io[0]
            bytes_recv_per_sec = net_io_counters.bytes_recv - previous_net_io[1]
            self.previous_net_io[proc.info['pid']] = (net_io_counters.bytes_sent, net_io_counters.bytes_recv)
            return bytes_sent_per_sec + bytes_recv_per_sec
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return 0

class NetworkMonitorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System & Network Monitor")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize segment monitors
        self.cpu_monitor = SegmentMonitor("CPU")
        self.memory_monitor = SegmentMonitor("Memory")
        self.disk_monitor = SegmentMonitor("Disk")
        self.network_monitor = SegmentMonitor("Network")
        self.gpu_monitor = SegmentMonitor("GPU")

        # Connect segment clicked signals to slot
        self.cpu_monitor.segment_clicked.connect(self.show_resource_details)
        self.memory_monitor.segment_clicked.connect(self.show_resource_details)
        self.disk_monitor.segment_clicked.connect(self.show_resource_details)
        self.network_monitor.segment_clicked.connect(self.show_resource_details)
        self.gpu_monitor.segment_clicked.connect(self.show_resource_details)

        # Create GUI layout
        self.initUI()

        # Start monitoring threads
        self.start_monitoring()

    def initUI(self):
        main_layout = QGridLayout()

        # Add widgets to grid layout
        main_layout.addWidget(self.cpu_monitor, 0, 0)
        main_layout.addWidget(self.memory_monitor, 0, 1)
        main_layout.addWidget(self.disk_monitor, 0, 2)
        main_layout.addWidget(self.network_monitor, 1, 0)
        main_layout.addWidget(self.gpu_monitor, 1, 1)

        self.setLayout(main_layout)

    def show_resource_details(self, segment_name):
        # Show the popup with process details for the clicked segment
        self.popup = ResourceDetailsPopup(segment_name)
        self.popup.show()

    def start_monitoring(self):
        # Start monitoring threads
        threading.Thread(target=self.monitor_system, daemon=True).start()
        threading.Thread(target=self.monitor_network, daemon=True).start()
        threading.Thread(target=self.monitor_gpu, daemon=True).start()

    def monitor_system(self):
        # Monitor CPU, Memory, and Disk usage
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            
            # Update the GUI with usage data
            self.cpu_monitor.update_usage(cpu_usage)
            self.memory_monitor.update_usage(memory_usage)
            self.disk_monitor.update_usage(disk_usage)
            
            time.sleep(1)

    def monitor_network(self):
        # Monitor total network bandwidth usage
        while True:
            net_io = psutil.net_io_counters()
            if net_io:
                # Convert total bytes to MB (divided by 1024*1024)
                total_bandwidth = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # MB
                self.network_monitor.update_usage(total_bandwidth)  # Update network monitor with total bandwidth in MB/s
            time.sleep(1)

    def monitor_gpu(self):
        # Monitor GPU usage
        while True:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_usage = gpus[0].load * 100  # GPU load is a value between 0 and 1
                self.gpu_monitor.update_usage(gpu_usage)
            else:
                self.gpu_monitor.update_usage(0)  # No GPU detected

            time.sleep(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    #app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    window = NetworkMonitorGUI()
    window.show()
    sys.exit(app.exec())
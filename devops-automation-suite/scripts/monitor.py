"""
Server Monitoring Script
Monitors server health and sends alerts
"""

import argparse
import psutil
import time
from datetime import datetime
from utils.logger import setup_logger
from utils.email_notifier import send_notification
from utils.config_loader import load_config

logger = setup_logger('monitor')


class ServerMonitor:
    """Server monitoring and alerting"""
    
    def __init__(self, config, alert_threshold=80):
        """
        Initialize server monitor
        
        Args:
            config: Configuration dictionary
            alert_threshold: Alert threshold percentage
        """
        self.config = config
        self.alert_threshold = alert_threshold
    
    def check_system(self):
        """Check system resources"""
        logger.info("=" * 60)
        logger.info(f"Server Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        alerts = []
        
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        logger.info(f"CPU Usage: {cpu_percent}%")
        
        if cpu_percent > self.alert_threshold:
            alerts.append(f"High CPU usage: {cpu_percent}%")
        
        # Memory Usage
        memory = psutil.virtual_memory()
        logger.info(f"Memory Usage: {memory.percent}%")
        logger.info(f"  Total: {self._format_bytes(memory.total)}")
        logger.info(f"  Available: {self._format_bytes(memory.available)}")
        logger.info(f"  Used: {self._format_bytes(memory.used)}")
        
        if memory.percent > self.alert_threshold:
            alerts.append(f"High memory usage: {memory.percent}%")
        
        # Disk Usage
        logger.info("\nDisk Usage:")
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                logger.info(f"  {partition.mountpoint}:")
                logger.info(f"    Total: {self._format_bytes(usage.total)}")
                logger.info(f"    Used: {self._format_bytes(usage.used)} ({usage.percent}%)")
                logger.info(f"    Free: {self._format_bytes(usage.free)}")
                
                if usage.percent > self.alert_threshold:
                    alerts.append(f"High disk usage on {partition.mountpoint}: {usage.percent}%")
            except PermissionError:
                continue
        
        # Network Stats
        logger.info("\nNetwork Stats:")
        net_io = psutil.net_io_counters()
        logger.info(f"  Bytes Sent: {self._format_bytes(net_io.bytes_sent)}")
        logger.info(f"  Bytes Received: {self._format_bytes(net_io.bytes_recv)}")
        
        # Process Count
        process_count = len(psutil.pids())
        logger.info(f"\nRunning Processes: {process_count}")
        
        # Top Processes by CPU
        logger.info("\nTop 5 Processes by CPU:")
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
        for proc in top_cpu:
            logger.info(f"  {proc['name']}: {proc['cpu_percent']}%")
        
        # Top Processes by Memory
        logger.info("\nTop 5 Processes by Memory:")
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        top_mem = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
        for proc in top_mem:
            logger.info(f"  {proc['name']}: {proc['memory_percent']:.2f}%")
        
        # Send alerts if needed
        if alerts:
            logger.warning("\n⚠️  ALERTS:")
            for alert in alerts:
                logger.warning(f"  - {alert}")
            
            send_notification(
                subject="Server Alert",
                body="\n".join(alerts),
                config=self.config
            )
        else:
            logger.info("\n✓ All systems normal")
        
        logger.info("=" * 60)
    
    def _format_bytes(self, bytes_value):
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def continuous_monitoring(self, interval=300):
        """
        Run continuous monitoring
        
        Args:
            interval: Check interval in seconds
        """
        logger.info(f"Starting continuous monitoring (interval: {interval}s)")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                self.check_system()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("\nMonitoring stopped")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Server Monitoring Script')
    parser.add_argument('--continuous', action='store_true',
                       help='Run continuous monitoring')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300)')
    parser.add_argument('--alert-threshold', type=int, default=80,
                       help='Alert threshold percentage (default: 80)')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.warning(f"Could not load configuration: {str(e)}")
        config = {}
    
    # Initialize monitor
    monitor = ServerMonitor(config, args.alert_threshold)
    
    # Run monitoring
    if args.continuous:
        monitor.continuous_monitoring(args.interval)
    else:
        monitor.check_system()


if __name__ == '__main__':
    main()
